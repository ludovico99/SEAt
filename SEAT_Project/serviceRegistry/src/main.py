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

    def getPortAndIp(self,request,context):
        try :
            self.sqlConn = sqlite3.connect(self.db_path)
            response = self.sqlConn.execute('SELECT * FROM serviceRegistry WHERE serviceName=?',(request.serviceName,)).fetchall()
            list = []
            if len(response) >= 1:
                for i in range (0,len(response)):
                    aux = grpc_pb2.registryResponse (serviceName = response[0][1],ip =response[0][2], port =response[0][3], hostname = response[0][4]) 
                    list.append(aux)
                return grpc_pb2.registryResponses (responses = list)
            else :
                aux = grpc_pb2.registryResponse (serviceName = "all",ip ="0.0.0.0", port = "0", hostname = "") 
                list.append (aux)
                return grpc_pb2.registryResponses (responses = list)
        except Exception as e:
            print(repr(e))
            list = []
            aux = grpc_pb2.registryResponse (serviceName = "all",ip ="0.0.0.0", port = "0", hostname = "") 
            list.append (aux)
            return grpc_pb2.registryResponses (responses = list)
            

    def receiveMessage (self):
        # Receive message from SQS queue
        try:
            while (True):
                time.sleep(0.5)
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
                    WaitTimeSeconds=15
                )

                if len(response) > 1:
                    message = response['Messages'][0]
                    body = response['Messages'][0]['Body']
                    print(body)
                    token = str(body).split(':')
                    port = token[1].split(',')[0]
                    ip = token[2].split(',')[0]
                    service_name = token[3].split(',')[0]
                    hostname= token[4][:-1]
                   
                    receipt_handle = message['ReceiptHandle']

                    # Delete received message from queue
                    self.sqs.delete_message(
                        QueueUrl=self.queue_name,
                        ReceiptHandle=receipt_handle
                    )
                    #print('Received and deleted message: %s' % message)

                    try :
                        self.sqlConn = sqlite3.connect(self.db_path)
                        result = self.sqlConn.execute('INSERT OR REPLACE INTO serviceRegistry (serviceName, ip_Addr, port, hostname) values (?,?,?,?)',(service_name,ip, port,hostname))
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
print('Starting SERVICE REGISTRY. Listening on port 50057.')
server.add_insecure_port('[::]:50057')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)