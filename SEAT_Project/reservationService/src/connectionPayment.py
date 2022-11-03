from connection import Connection
from dBUtils import DBUtils
from proto import grpc_pb2
from proto import grpc_pb2_grpc
from decimal import Decimal
from connectionEmail import ConnectionEmail
import boto3
import uuid
import pika

class ConnectionPayment (Connection):
    def __init__(self, stubAccounting):
        self.db = DBUtils()
        self.stubAccounting = stubAccounting
        dynamoDb = boto3.resource('dynamodb', region_name='us-east-1')
        self.responseMsg = "" 


    def payOnline(self, id, username, email, lido_id, costo, distance, budgetDifference, idCard):
        """Trigger the SAGA transaction: reservation -> payment -> update of user's history

        Returns:
            BOOL: True if the payment transaction succeded
            String: error message
        """
        # crea una connessione
        result,errorMsg = self.establishConnection ()
        if result == False:
            return result, errorMsg
        
        # pubblica un messaggio  per triggerare il pagamento
        request = "{}:{}:{}:{}:{}:{}:{}:{}".format (id,username, email, lido_id, costo, distance, budgetDifference, idCard)
        print("SENDING A PAYMENT REQUEST TO {} WITH EMAIL {}".format(username, email))
        self.publish(request, 'Pay_request')

        # si mette in attesa che la transazione finisca. Viene sbloccato dall'ultima callback
        self.channel.start_consuming()
        print("END SAGA")
        
        ret = True
        if len(self.responseMsg)!=0:
            ret = False
        return ret, self.responseMsg



    def publish(self, request, routingKey):
        """Utility function to publish a message in the specified queue

        Args:
            request (String): body of the message to publish
            routingKey (String): name of queue to publish the message
        """
        print (request, routingKey)        
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=routingKey,
            properties=pika.BasicProperties(
                correlation_id=self.corr_id,
            ),
            body=request)



    def on_channel_open (self):
        """Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print("CHANNEL CORRECTLY CREATED")
            
            # Dichiarazione per le code delle richieste e delle risposte
            self.channel.queue_declare(queue="Pay_request")
            self.channel.queue_declare(queue="Pay_response") 
        
            self.channel.queue_declare(queue="History_request")
            self.channel.queue_declare(queue="History_response")
            
            self.publishRequest = "History_request"
            
            
            # quando consuma da History_request deve eseguire l'update della storia utente
            self.channel.basic_consume(
                    queue="History_request",
                    on_message_callback=self.updateUserHistory,
                    auto_ack=True)

            # quando consuma da pay_response valuta se eseguire il rollback oppure no
            self.channel.basic_consume(
                    queue="Pay_response",
                    on_message_callback=self.onResponseSaga,
                    auto_ack=True)

            return True

        except Exception as e:
            print(repr(e))
            if (self.connection != None):
                self.connection.close()
            return False

    def updateUserHistory(self, ch, method, properties, body):
        """CALLBACK FUNCTION: perform the update of the user's history (only if payment succeded). 
        The table "storiaUtente" contains details about previous reservation performed by user:
        information inserded here are used in suggestion algorithm.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed

        """
        
        print("\nUPDATE USER HISTORY phase has started: from History_request to History_response")
        try:
            request = body.decode("utf-8").split(':')
            id = request[0]
            username = request[1]
            email = request[2]
            lido_id = request[3]
            costo = int(request[4])
            distance = float(request[5])
            budgetDifference=float(request[6])
            cardId = int(request[7])

            print("[Storia utente] Username:{}, distanza:{}, differenza dal budget: {}".format (
                    username, distance, budgetDifference))

            
            # 1. Leggi i valori della tabella per l'utente, se esistono
            data = self.db.scanDb('storiaUtente', ['userId'], [username])
            
            # 2. se non esistono valori inizializzo tutto a 0
            if len(data) == 0:
                mediaDistanza = mediaDifferenzaBudget = 0.0
                varianzaDistanza = varianzaDifferenzaBudget = 0.
                counter = 0
                nRistorazione = nBar = nCampi = nAnimazione = nPalestra = 0
            else:
                mediaDistanza = float(data[0]['mediaDistanza'])
                varianzaDistanza = float(data[0]['varianzaDistanza'])
                mediaDifferenzaBudget = float(data[0]['mediaDifferenzaBudget'])
                varianzaDifferenzaBudget = float(data[0]['varianzaDifferenzaBudget'])
                counter = int(data[0]['tot'])
                nRistorazione = data[0]['nRistorazione']
                nBar = data[0]['nBar']
                nCampi = data[0]['nCampi']
                nAnimazione = data[0]['nAnimazione']
                nPalestra = data[0]['nPalestra']
            
            # 3. incrementa il contatore delle caratteristiche che l'utente ha scelto nei lidi

            responseAccounting = self.stubAccounting.getBeachClubDetails(grpc_pb2.reviewRequest(usernameBeachClub=lido_id))
            if responseAccounting.ristorazione == True:
                nRistorazione = nRistorazione + 1
            if responseAccounting.bar == True:
                nBar = nBar +1
            if responseAccounting.campi == True:
                nCampi = nCampi +1
            if responseAccounting.animazione == True:
                nAnimazione = nAnimazione + 1
            if responseAccounting.palestra == True:   
                nPalestra = nPalestra + 1
            
            # 4. aggiorna le medie e le varianze
            varianzaDistanza = varianzaDistanza + (counter/(counter+1))*((distance-mediaDistanza)**2)
            varianzaDifferenzaBudget = varianzaDifferenzaBudget + (counter/(counter+1))*((budgetDifference-mediaDifferenzaBudget)**2)

            mediaDistanza = mediaDistanza + (distance-mediaDistanza)/(counter+1)
            mediaDifferenzaBudget = mediaDifferenzaBudget + (budgetDifference-mediaDifferenzaBudget)/(counter+1)
            
            counter = counter + 1
            

            # 5. aggiorna le entry nel database per le recommendation
            
            update = self.db.updateTransaction([['userId','S',username]],[['mediaDistanza','N',mediaDistanza],['varianzaDistanza','N',varianzaDistanza],['mediaDifferenzaBudget','N',mediaDifferenzaBudget],['varianzaDifferenzaBudget','N',varianzaDifferenzaBudget],
            ['tot','N',counter],['nRistorazione','N',nRistorazione],['nBar','N',nBar],['nCampi','N',nCampi],['nAnimazione','N',nAnimazione],['nPalestra','N',nPalestra]],"storiaUtente")
            
        
            response,msg = self.db.executeTransaction([update])

            if response == False:

                print("[Update user history]:", msg)
                request = "FAILURE:{}:{}:{}:{}:{}:{}:{}".format(id,username,email,lido_id,costo,cardId,msg)
                
                self.publish(request, 'History_response')

            else :
            
                msg = "Saga completed correctly"
                print("[Update user history]:", msg)
                request = "SUCCESS:{}:{}:{}:{}:{}:{}:{}".format(id,username,email,lido_id,costo,cardId,msg)
                
                self.publish(request, 'History_response')

        except Exception as e:
            print(repr(e))
            errorMsg = "Update user history operation has failed"
            request = "FAILURE:{}:{}:{}:{}:{}:{}:{}".format(id,username,email,lido_id,costo,cardId,errorMsg)
            self.publish(request, 'History_response')


    def onResponseSaga (self, ch, method, properties, body):
        """ CALLBACK FUNCTION: complete the SAGA transaction sending the reservation's confirmation email.
        If the transaction failed perform the ROLLBACK of the reservation.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
        try:
            #RESPONSE-> SUCCESS:Prenotazione_ID:username:Email:msg 
            response = body.decode("utf-8").split(':')
            print("\nRESPONSE Saga from Pay_response: {}".format(response))
            esito = str(response[0])
            prenotazione_id = int(response[1])
            username = response[2]
            email = response[3]
            msg = response[4] 
            
            self.responseMsg = msg
            if (esito != "SUCCESS"):

                # 1. fare il rollback dell'inserimento della prenotazione
                print("ROLLBACK operation: Deleting reservation previously inserted")
                data = self.db.scanDb('prenotazione', ['prenotazioneId'], [prenotazione_id])
                print("1")
                transactions = []
                for i in range (0,len(data)) :
                    delete = self.db.deleteTrasaction([['prenotazioneId','N',prenotazione_id],['ombrelloneId','S',data[i]['ombrelloneId']]],"prenotazione")
                    transactions.append(delete)
                
                print(transactions)
                response,msg = self.db.executeTransaction(transactions)
                
            
            else:   
                # 2. lascio alla classe connectionEmail la complessità della gestione delle code
                connessione = ConnectionEmail()
                result, errorMsg = connessione.sendEmail (username, email)
                print ("result:{}, ErrorMsg:{}".format(result, errorMsg))
            
        
        except Exception as e:
            print(repr(e))
            
        finally:

            # SBLOCCO il metodo bloccato in modo da far terminare in modo sicrono la RPC
            if self.channel != None:
                self.channel.stop_consuming()
            
            # chiusura della connessione
            if self.connection != None and self.connection.is_open:
                    self.connection.close()  
    
            
