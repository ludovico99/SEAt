from connection import Connection
import uuid
import pika

# PENSO CHE QUESTA CLASSE POSSA ESSERE ELIMINATA

class ConnectionEmail (Connection):
    def __init__(self):
        self.corr_id = None
        self.requestQueue = None
        self.responseQueue = None
    

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
                return False, "Error in establishing connection phase"

            request = "{}:{}#Accounting".format (username,email)
            #INVIO DEL MESSAGGIO DI RICHIESTA
            print("SENDING AN EMAIL TO {}".format(request))
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='',
                routing_key='emailQueue',
                properties=pika.BasicProperties(
                    reply_to=self.responseQueue,
                ),
                body=request)

            self.connection.process_data_events(time_limit=None)
            
        except Exception as e:
            print(repr(e))
            return False , "Send operation has failed"
        return True, "Send operation has succeded"
    

    

    def onResponse(self,ch,method,properties,body):
        """ CALLBACK FUNCTION for the response message from the email service

        Args:
            ch (BlockingChannel): Instance of Blocking channel over which the communication is happening
            method (Delivery): meta information regarding the message delivery
            properties (BasicProperties): user-defined properties on the message
            body (string): body of the message
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
        """Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print('Have exchange')

            result = self.channel.queue_declare(queue="emailQueue")
            self.requestQueue = result.method.queue

            result =self.channel.queue_declare(queue='responseQueue:Accounting')
            self.responseQueue = result.method.queue

            #BINDING DELLA CODA delle risposte all'exchange con routing key pari a Payment
            self.channel.queue_bind(exchange='topic_logs', queue=self.responseQueue, routing_key="Accounting.*")
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
                    on_message_callback=self.onResponse,
                    auto_ack=True)

            print("Awaiting email responses")
            return True
        except Exception as e:
            print(repr(e))
            if self.connection != None:
                self.connection.close()
            return False

    