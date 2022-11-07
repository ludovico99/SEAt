from proto import grpc_pb2
from proto import grpc_pb2_grpc
import grpc
import time
from concurrent import futures
import sqlite3
import boto3

class ServiceRegistryServicer(grpc_pb2_grpc.ServiceRegistryServicer):

      def __init__(self):
        self.sqlConn = None

        self.sqs = boto3.resource('sqs', region_name='us-east-1')

        self.client = boto3.client('sqs', region_name='us-east-1')

        try:
            self.sqlConn = sqlite3.connect('serviceRegistry/src/registry.db')
            
            with open("serviceRegistry/src/createDB.sql","r") as f:
                self.sqlConn.executescript(f.read())
            self.sqlConn.commit()

        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_ReviewServicer_to_server(ServiceRegistryServicer(), server)
print('Starting SERVICE REGISTRY. Listening on port 50056.')
server.add_insecure_port('[::]:50056')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)