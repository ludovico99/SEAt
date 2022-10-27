from symbol import parameters
import pika
import time
import socket
import os
from functools import partial

class EmailService (object):

    def __init__(self):
    
            #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.connection = None
        self.channel = None
        self.exchange = "topic_logs"
        # while self.connection is None:
        try:
            amqp_url = os.environ['AMQP_URL']

            # Actually connect
            # credentials = pika.PlainCredentials(username="guest", password="guest")
            parameters = pika.URLParameters(amqp_url)
            self.connection = pika.BlockingConnection(parameters) 
            # self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_open)

            # Main loop.  This will run forever, or until we get killed.
            #self.connection.ioloop.start()

            self.on_open ()
            
            # self.connection = pika.BlockingConnection(
            # pika.ConnectionParameters(host='rabbitmq:5672'))
        # except socket.gaierror as error:
        #     print("SONO QUI")
        #     time.sleep(1)

        except KeyboardInterrupt:
            if (self.connection != None):
                self.connection.close()
                #self.connection.ioloop.start
                    
        except Exception as e:
            print(repr(e))
    


    def on_open (self):
        try:
            print ("CONNECTION OPEN")
            
            self.channel = self.connection.channel()
            self.on_channel_open()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
        #self.channel.start_consuming()
    
    def on_channel_open (self):
        try:
            print ("CHANNEL OPEN")
            self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
            self.on_exchange ()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()

        
    def on_exchange(self):
        try :
            print('Have exchange')
            #CODA PER LE RICHIESTE PROVENIENTI DALL'ACCOUNT
            result = self.channel.queue_declare(queue='emailQueue')
            self.requestQueue = result.method.queue

            self.on_queue()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()

    def on_queue(self):
        try:
            print('Have queue')

            # This call tells the server to send us 1 message in advance.
            # This helps overall throughput, but it does require us to deal
            # with the messages we have promptly.
            self.channel.basic_qos(prefetch_count=1)
            self.on_qos()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()


    def on_qos(self):
        try:
            print('Set QoS')
            self.channel.queue_bind(queue=self.requestQueue, exchange=self.exchange)
            self.on_bind()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            


    def on_bind(self):
        """Callback when we have successfully bound the queue to the exchange."""
        print('Bound')
        self.channel.basic_consume(
                queue=self.requestQueue,
                on_message_callback=self.onRequest,
                auto_ack=True)

        print("Starting EMAIL SERVICE. [x] Awaiting email requests")
        self.channel.start_consuming()

        

    def onRequest(self,ch,method,props,body):
        try:
            
            #TODO SEND EMAIL
            tokens = body.decode("utf-8").split('#')
            print("\nREQUEST: {}".format(tokens))
            toQueue = tokens[-1]
            print (tokens[-1])

            message = "EMAIL has been sent to {}".format(str(body))
            if toQueue == "Accounting":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Accounting.response", body=message)
            elif toQueue == "Reservation":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Reservation.response", body=message)
            elif toQueue == "Payment":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Payment.response", body=message) 

        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
        
        
print("Starting EMAIL SERVICE. [x] BEFORE INIT")

emailService = EmailService()

