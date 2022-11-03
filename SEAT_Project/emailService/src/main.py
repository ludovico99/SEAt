from symbol import parameters
import pika
import time
import socket
import os
from functools import partial

class EmailService (object):

    def __init__(self):
    
        self.connection = None
        self.channel = None
        self.exchange = "topic_logs"

        try:
            amqp_url = os.environ['AMQP_URL']
            parameters = pika.URLParameters(amqp_url)
            self.connection = pika.BlockingConnection(parameters) 
            self.on_open ()
            
        except KeyboardInterrupt:
            if (self.connection != None):
                self.connection.close()
                    
        except Exception as e:
            print(repr(e))
    

    def on_open (self):
        """create a new channel

        Returns:
            BOOL: return TRUE if the channel creation has succeded
        """
        try:
            print ("CONNECTION OPEN")
            
            self.channel = self.connection.channel()
            return self.on_channel_open()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False

    def on_channel_open (self):
        """ declare the exchange (type=topic) after channel creation. The exchange is called "topic_logs". 

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print ("CHANNEL OPEN")
            self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
            return self.on_exchange ()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False

        
    def on_exchange(self):
        """ Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try :
            print('Have exchange')
            #CODA PER LE RICHIESTE PROVENIENTI DALL'ACCOUNT
            result = self.channel.queue_declare(queue='emailQueue')
            self.requestQueue = result.method.queue

            return self.on_queue()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False

    def on_queue(self):
        try:
            print('Have queue')

            # This call tells the server to send us 1 message in advance.
            # This helps overall throughput, but it does require us to deal
            # with the messages we have promptly.
            self.channel.basic_qos(prefetch_count=1)
            return self.on_qos()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False


    def on_qos(self):
        try:
            print('Set QoS')
            self.channel.queue_bind(queue=self.requestQueue, exchange=self.exchange)
            return self.on_bind()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False
            


    def on_bind(self):
        """ define the CALLBACK FUNCTION

        Returns:
            BOOL: outcome of the definition
        """
        try:
            print('Bound')
            self.channel.basic_consume(
                queue=self.requestQueue,
                on_message_callback=self.onRequest,
                auto_ack=True)

            print("Starting EMAIL SERVICE. [x] Awaiting email requests")
            self.channel.start_consuming()
            return True
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False
        

    def onRequest(self,ch,method,props,body):
        """CALLBACK FUNCTION that simulate the email sending

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
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

