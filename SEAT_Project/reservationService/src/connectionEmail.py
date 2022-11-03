from connection import Connection
import uuid
import pika

class ConnectionEmail (Connection):
    def __init__(self):
        self.corr_id = None
    

    def sendEmail(self, username, email):
        """Send email to the user specified (Asynchronous communication with the email microservice)

        Args:
            username (String): user to send the main
            email (String): user's email

        Returns:
            BOOL: outcome of the sending operation
            String: message
        """
        try :
            result = self.establishConnection ()
            if result == False:
                return False

            #INVIO DEL MESSAGGIO DI RICHIESTA
            request = "{}:{}#Reservation".format (username,email)
            print("SENDING AN EMAIL TO {}".format(request))
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='',
                routing_key='emailQueue',
                properties=pika.BasicProperties(
                    correlation_id=self.corr_id,
                ),
                body=request)

            self.connection.process_data_events(time_limit=None)
        except Exception as e:
            print(repr(e))
           
            return False , "Send operation has failed"
        return True, "Send operation has succeded"
    

    def onResponseEmail (self, ch, method, properties, body):
        """CALLBACK FUNCTION: close the connection opened to stop the communication
        (when receiving the response from EMAIL SERVICE)

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
        print("RESPONSE: %r:%r" % (method.routing_key, body))
        if self.connection != None and self.connection.is_open:
            self.connection.close()
    

    def on_channel_open (self):
        """ declare the exchange (type=topic) after channel creation. The exchange is called "topic_logs". 

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print("CHANNEL OPEN")
            self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
            return self.on_exchange()
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False

    def on_exchange (self):
        """ Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print('Have exchange')

            #CODA PER TUTTE LE RICHIESTE
            result = self.channel.queue_declare(queue="emailQueue")
            self.requestQueue = result.method.queue

            #CODA PER LE RISPOSTE
            result = self.channel.queue_declare(queue='responseQueue:Reservation') 
            self.responseQueue = result.method.queue

            #BINDING DELLA CODA delle risposte all'exchange con routing key pari a Reservation
            self.channel.queue_bind(exchange='topic_logs', queue=self.responseQueue, routing_key="Reservation.*")
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
            self.channel.basic_consume(
                    queue=self.responseQueue,
                    on_message_callback=self.onResponseEmail,
                    auto_ack=True)

            print("Awaiting email responses")
            return True
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False
    
        


    