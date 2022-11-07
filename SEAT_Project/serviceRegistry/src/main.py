from proto import grpc_pb2
from proto import grpc_pb2_grpc
import grpc
import time
from concurrent import futures
import sqlite3
import boto3
import os

class ServiceRegistryServicer(grpc_pb2_grpc.ServiceRegistryServicer):

    def __init__(self):
        self.sqlConn = None
        
        try:
           
            self.sqs = boto3.client('sqs', region_name='us-east-1')
            self.queue_name = "service_registry_queue"
            self.db_path = '{}/registry.db'.format(os.path.dirname(__file__))
            self.sqlConn = sqlite3.connect(self.db_path)
            if (self.sqlConn != None):
                with open("{}/createDB.sql".format(os.path.dirname(__file__)),"r") as f:
                    self.sqlConn.executescript(f.read())
                
                self.sqlConn.commit()

            response,msg= self.receiveMessage ()
            print(msg)

        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()

    def receiveMessage (self):
        # Receive message from SQS queue
        try:
            while (True):
                time.sleep(1)
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_name,
                    AttributeNames=[
                        'SentTimestamp'
                    ],
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=[
                        'All'
                    ],
                    VisibilityTimeout=0,
                    WaitTimeSeconds=20
                )

                if len(response) > 1:
                    message = response['Messages'][0]
                    body = response['Messages'][0]['Body']
                    print(body)
                    token = str(body).split(':')
                    print(token)
                    port = token[1].split(',')[0]
                    ip = token[2].split(',')[0]
                    service_name = token[3][:-1]
                    print("service name : {}, ip: {}, port: {}".format(service_name,ip,port))

                    receipt_handle = message['ReceiptHandle']

                    # Delete received message from queue
                    self.sqs.delete_message(
                        QueueUrl=self.queue_name,
                        ReceiptHandle=receipt_handle
                    )
                    #print('Received and deleted message: %s' % message)

                    try :
                        self.sqlConn = sqlite3.connect(self.db_path)
                        result = self.sqlConn.execute('INSERT OR REPLACE INTO payment (username,ip_Addr,port) values (?,?,?)',(service_name,ip, port))
                        self.sqlConn.commit()
                    except Exception as e:
                        print(repr(e))

                else :
                    break
                    
            return True,"All Messages received and deleted correctly"
        except self.sqs.exceptions.OverLimit as e:
            print(repr(e))
            return False, "Message not received"
        except Exception as e :
            print(repr(e))
            return False, "An error has occured in the delete message operation"




server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_ServiceRegistryServicer_to_server(ServiceRegistryServicer(), server)
print('Starting SERVICE REGISTRY. Listening on port 50056.')
server.add_insecure_port('[::]:50056')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)