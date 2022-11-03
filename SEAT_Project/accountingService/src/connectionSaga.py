from connection import Connection
from proto import grpc_pb2
from proto import grpc_pb2_grpc
from connectionEmail import ConnectionEmail
from dBUtils import DBUtils
import uuid
import pika

class ConnectionSaga (Connection):
    
    def __init__(self):
        self.db = DBUtils()
        self.msg = ""
        self.outcome = None

    
    def deleteAccount(self, username, isAdmin):
        """Trigger the SAGA transaction: removal "payment card -> user's data"

        Returns:
            BOOL: True if the transaction succeded   ???
            String: error message
        """
        # crea una connessione
        res, msg = self.establishConnection()
        if res == False:
            return res, "Error in connection"
        
        # pubblica un messaggio  per triggerare la delete
        request = "{}:{}".format(username, isAdmin)
        print("SENDING A DELETE REQUEST")
        self.channel.basic_publish(
            exchange='', 
            routing_key= "Payment_request", 
            properties=pika.BasicProperties(
                    reply_to= "Account_response",
                ),
            body=request
        )
        # si mette in attesa che la transazione finisca. Viene sbloccato dall'ultima callback        
        self.channel.start_consuming()
            
        print("END")
        return self.outcome, self.msg


    def on_channel_open (self):
        """Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """

        try:
            print("CHANNEL CORRECTLY CREATED")

            # Dichiarazione per le code delle richieste e delle risposte per DELETE ACCOUNT
            self.channel.queue_declare(queue="Account_request")
            self.channel.queue_declare(queue="Account_response")

            self.channel.queue_declare(queue="Payment_request")
            self.channel.queue_declare(queue="Payment_response") 
            
            # quando consuma da Account_request valuta se effettuare l'eliminazione dei dati in base all'esito dell'eliminazione della carta di pagamento
            self.channel.basic_consume(
                    queue="Account_request",
                    on_message_callback=self.onDeleteRequest,
                    auto_ack=True)
            
            # quando consuma da Account_response finalizza l'eliminazione
            self.channel.basic_consume(
                    queue="Account_response",
                    on_message_callback=self.onDeleteResponse,
                    auto_ack=True)

            return True

        except Exception as e:
            print(repr(e))
            if (self.connection != None):
                self.connection.close()
            return False
    

    def onDeleteResponse (self,ch,method,properties,body):
        """ CALLBACK FUNCTION that finalize the account's removal

        Args:
            ch (BlockingChannel): Instance of Blocking channel over which the communication is happening
            method (Delivery): meta information regarding the message delivery
            properties (BasicProperties): user-defined properties on the message
            body (string): body of the message
        """
        try:
            
            #request = "{}:{}:{}".format(username,admin,"DELETE operation ended successfully")  
            response = body.decode("utf-8").split(':')
            esito = response[0]
            if esito == SUCCESS:
                self.msg = "Email sent"
                self.outcome = False
            else:
                self.msg = "Email sending failed"
                self.outcome = True
            print("\nMessage from Payment_response: {}".format(response))
            print("ROUTING TO: {}".format(properties.reply_to))

        except Exception as e:
            print(repr(e))

        finally:
            if self.channel != None:
                self.channel.stop_consuming()
            if self.connection != None and self.connection.is_open:
                self.connection.close()


    def onDeleteRequest (self, ch, method, properties, body):

        """CALLBACK FUNCTION that perform the removal of user's data only when the payment card's removal has succeded.

        Args:
            ch (BlockingChannel): Instance of Blocking channel over which the communication is happening
            method (Delivery): meta information regarding the message delivery
            properties (BasicProperties): user-defined properties on the message
            body (string): body of the message

        """

        try:
            #request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in payment service has succeded",list)
            response = body.decode("utf-8").split(':')
            print("\nMessage from Payment_request queue: {}".format(response))
            esito = str(response[0])
            username = response[1]
            admin = bool(response[2])
            msg = str(response[3])
            list = response[4]

            print(properties.reply_to)
            
            if esito == "SUCCESS":
                print("Payment service has completed successfully, trying to delete the remaining ones (entries)")

                transactions = []
                delete = self.db.deleteTrasaction([['username','S',username]],'utenti')
            
                transactions.append (delete)

                if  admin == True: 
                    delete = self.db.deleteTrasaction([['username','S',username]],'dettagliLido')
          
                    transactions.append (delete)
                            
                data = self.db.scanDb("postazioniPerFila", ['lidoId'], [username])

                if data == None:
                    return

                for i in range (0,len(data)):
                    tmp = i+1
                    delete = self.db.deleteTrasaction([['lidoId','S',username],['numeroFila','N',tmp]],'postazioniPerFila')
                
                    transactions.append(delete)

                delete = self.db.deleteTrasaction([['userId','S',username]],'storiaUtente')
           
                transactions.append (delete)
                data = self.db.scanDb("prenotazione", ['lidoId'], [username])
                if data == None:
                    return

                for i in range (0, len(data)):
                    delete = self.db.deleteTrasaction([['prenotazioneId','N',data[i]['prenotazioneId']],['ombrelloneId','S',data[i]['ombrelloneId']]],'prenotazione')
            
                    transactions.append(delete)

                data = self.db.scanDb('pricePerSeason', ['lidoId'], [username])
                if data == None:
                    return

                for i in range (0, len(data)):
                    delete = self.db.deleteTrasaction([['lidoId','S',data[i]['lidoId']],['season','S',data[i]['season']]],'pricePerSeason')
                
                    transactions.append(delete)

                data = self.db.scanDb('pricePerRow', ['lidoId'], [username])
                if data == None:
                    return 

                for i in range (0, len(data)):
                    delete = self.db.deleteTrasaction([['lidoId','S',data[i]['lidoId']],['row','S',data[i]['row']]],'pricePerRow')
                  
                    transactions.append(delete)

                data = self.db.scanDb('pricePerPiece', ['lidoId'], [username])
                if data == None:
                    return 

                for i in range (0, len(data)):
                    delete = self.db.deleteTrasaction([['lidoId','S',data[i]['lidoId']],['pezzo','S',data[i]['pezzo']]],'pricePerPiece')
                
                    transactions.append(delete)

                data = self.db.scanDb('recensioni', ['lidoId'], [username])
                if data == None:
                    return 

                for i in range (0, len(data)):
                    delete = self.db.deleteTrasaction([['recensioneId','N',data[i]['recensioneId']]],'recensioni')
                  
                    transactions.append(delete)

                print(transactions)
                
                response,msg = self.db.executeTransaction(transactions)

                if response == False:
                    request = "FAILURE:{}:{}:{}:{}".format(username,admin,msg,list)        

                    self.channel.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                  
                    body=request)
                    
                request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in account service has succeded",list)       

                self.channel.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                body=request)
                

        except Exception as e:
            print(repr(e))
            request = "FAILURE:{}:{}:{}:{}".format(username,admin,"Delete in account service has failed",list)
            self.channel.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                    body=request)

    