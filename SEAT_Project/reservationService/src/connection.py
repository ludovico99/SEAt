from abc import ABC, abstractmethod
import pika
import os

class Connection(ABC):
    
    def __init__(self):
        self.connection = None
        self.channel = None
    
    

    def establishConnection (self):
        """ Create a new instance of the Connection Object for RabbitMQ
        

        Returns:
            BOOL: return TRUE if the connection to RabbitMQ server has succeded
        """
        try :
            amqp_url = os.environ['AMQP_URL']

            parameters = pika.URLParameters(amqp_url)
            self.connection = pika.BlockingConnection(parameters)
            
            return self.on_open(),"Connection and queues are correctly established"
        
        except KeyboardInterrupt:
            if (self.connection != None):
                self.connection.close()
       
        except Exception as e:
            print(repr(e))
        return False,"Error in establishing connections and queues"
    
    

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

    
    
    @abstractmethod
    def on_channel_open(self):
        """Define request and response queues
        """
        pass