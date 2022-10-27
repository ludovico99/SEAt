import pika
import time
import socket
import os
from functools import partial

class EmailService (object):

    def __init__(self):
        try :
            #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.connection = None
            self.channel = None
            self.exchange = "topic_logs"
            # while self.connection is None:
            try:
                amqp_url = os.environ['AMQP_URL']

                    # Actually connect
                parameters = pika.URLParameters(amqp_url)
                self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_open)

                # Main loop.  This will run forever, or until we get killed.
                self.connection.ioloop.start()
                
                # self.connection = pika.BlockingConnection(
                # pika.ConnectionParameters(host='rabbitmq:5672'))
            # except socket.gaierror as error:
            #     time.sleep(1)

            except KeyboardInterrupt:
                if (self.connection != None):
                    self.connection.close()
                    self.connection.ioloop.start
                        
        except Exception as e:
            print(repr(e))
            self.errorMsg = "Error in establishing connections and queues"
    

    def on_open (self):
        self.channel = self.connection.channel(self.on_channel_open)
    
    def on_channel_open (self):
        self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic',callback = partial (self.on_exchange,self.channel))

        
    def on_exchange(self,channel):
        print('Have exchange')
        #CODA PER LE RICHIESTE PROVENIENTI DALL'ACCOUNT
        result = channel.queue_declare(queue='emailQueue',callback= partial(self.on_queue,channel))
        self.requestQueue = result.method.queue

    def on_queue(self,channel):

        print('Have queue')

        # This call tells the server to send us 1 message in advance.
        # This helps overall throughput, but it does require us to deal
        # with the messages we have promptly.
        channel.basic_qos(prefetch_count=1, callback= partial(self.on_qos,channel))


    def on_qos(self,channel):
    
        print('Set QoS')
        channel.queue_bind(queue=self.requestQueue, exchange=self.exchange,
                        callback= partial(self.on_bind,channel))


    def on_bind(self,channel):
        """Callback when we have successfully bound the queue to the exchange."""
        print('Bound')
        channel.basic_consume(
                queue=self.requestQueue,
                on_message_callback=self.onRequest,
                auto_ack=True)

        self.channel.start_consuming()



    def onRequest(self,ch,method,props,body):
        if props.correlation_id != None :
            print("REQUEST: %r:%r" % (props.correlation_id, body))
            #TODO SEND EMAIL
            tokens = str(body).split('#')
            toQueue = tokens[-1][:-1]
            print (tokens[-1][:-1])

            message = "EMAIL has been sent to {}".format(str(body))
            if toQueue == "Accounting":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Accounting.response", body=message)
            elif toQueue == "Reservation":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Reservation.response", body=message)
            elif toQueue == "Payment":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Payment.response", body=message) 

        self.channel.basic_ack(method.delivery_tag)
        
print("Starting EMAIL SERVICE. [x] BEFORE INIT")
emailService = EmailService()
print("Starting EMAIL SERVICE. [x] Awaiting email requests")
# emailService.channel.start_consuming()