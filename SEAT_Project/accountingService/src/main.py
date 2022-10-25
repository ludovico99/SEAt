from concurrent import futures
import threading
import time
import grpc
import uuid
import pika

from dBUtils import DBUtils

from proto import grpc_pb2
from proto import grpc_pb2_grpc


class AccountingServicer(grpc_pb2_grpc.AccountingServicer):
    
    def __init__(self):
        """Costructor for Accounting service class
        """
        self.errorMsg = ""
        self.connection = None
        self.channel = None
        self.corr_id = None
        self.requestQueue = None
        self.responseQueue = None

        self.connectionSAGA = None
        self.channelSAGA = None

        self.db = DBUtils()
    
        self.establishConnectionSAGA()


    def establishConnectionSAGA (self):
        """  Create a new instance of the Connection Object for RabbitMQ, then create a new channel and declares request and response queues
             for implementing Saga pattern

        Returns:
            BOOL,String: Return a Boolean in order to discriminate the success or failure of the method and an error message
        """
        try :
            self.connectionSAGA = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq:5672'))

            self.channelSAGA = self.connectionSAGA.channel()

            # Dichiarazione per le code delle richieste e delle risposte
            self.channelSAGA.queue_declare(queue="Account_request")
            self.channelSAGA.queue_declare(queue="Account_response")

            self.channelSAGA.queue_declare(queue="Payment_request")
            self.channelSAGA.queue_declare(queue="Payment_response")

            # #Exchange di ricezione e binding
            # self.channelSAGA.exchange_declare(exchange='topic_logs_2', exchange_type='topic')

            # self.channelSAGA.queue_bind(exchange='topic_logs_2', queue='Account_request', routing_key="Account.request.*")
            # self.channelSAGA.queue_bind(exchange='topic_logs_2', queue='Account_response', routing_key="Account.response.*")

            # #Exchange di invio
            # self.channelSAGA.exchange_declare(exchange='topic_logs_1', exchange_type='topic')

            self.channelSAGA.basic_consume(
                    queue="Account_request",
                    on_message_callback=self.onDeleteRequest,
                    auto_ack=True)

            self.channelSAGA.basic_consume(
                    queue="Account_response",
                    on_message_callback=self.onDeleteResponse,
                    auto_ack=True)


        except Exception as e:
            print(repr(e))
            if self.connectionSAGA != None:
                self.connectionSAGA.close()
            return False,"Error in establishing connections and queues"
        return True,"Connection and queues are correctly established "

    def onDeleteResponse (self,ch,method,properties,body):
        """ Callback function for messages that tell if the delete operation has succeded or not

        Args:
            ch (BlockingChannel): Instance of Blocking channel over which the communication is happening
            method (Delivery): meta information regarding the message delivery
            properties (BasicProperties): user-defined properties on the message
            body (string): body of the message
        """
        try:
            #request = "{}:{}:{}".format(username,admin,"DELETE operation ended successfully")  
            response = body.decode("utf-8").split(':')
            print("\nMessage from Payment_response: {}".format(response))
        
        except Exception as e:
            print(repr(e))
        finally: 
            if self.connectionSAGA != None and self.connectionSAGA.is_open:
                self.connectionSAGA.close()

    def onDeleteRequest (self, ch, method, properties, body):

        """Callback function for messages that tell if the delete in the payment private database has succeded or not

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
            self.response = True

            print(properties.reply_to)
            
            if esito == "SUCCESS":
                print("Payment service has completed successfully, trying to delete the remaining ones (entries)")

                self.response = True
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

                    self.channelSAGA.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                  
                    body=request)
                    
                request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in account service has succeded",list)       

                self.channelSAGA.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                body=request)

        except Exception as e:
            print(repr(e))
            request = "FAILURE:{}:{}:{}:{}".format(username,admin,"Delete in account service has failed",list)
            self.channelSAGA.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(
                        reply_to= "Account_response",
                    ),
                    body=request)
            

    def registerAccount(self, registrationRequest, context):
        """ Register a new Account (Admin or normal user) in dynamoDB

        Args:
            registrationRequest (grpc_pb2.registrationRequest): GRPC auto-generated registrationRequest message. 
            It contains the credentials of the user
            context (_type_): context information 

        Returns:
            grpc_pb2.response: GRPC auto-generated response message that tells if the registration has succeded and 
            a string that describes the state of the operation
        """
        
        print("Server has received:")
        print(registrationRequest.username, registrationRequest.password, registrationRequest.email, registrationRequest.admin)
        if registrationRequest.admin == True:
            opt = registrationRequest.opt
            print(opt.beachClubName, opt.location, opt.cardId)

        result,errorMsg = self.insertAnUser(registrationRequest)
        response = grpc_pb2.response(operationResult = result, errorMessage = errorMsg)
        return response

    def login(self, loginRequest, context):

        """ Login procedure to the system

        Args:
            loginRequest (grpc_pb2.loginRequest): GRPC auto-generated loginRequest message. 
            It contains the credentials of the user
            context (_type_): context information 

        Returns:
            grpc_pb2.session: GRPC auto-generated session message that contains the credentials if the user has been successfully logged in the system
        """

        
        print("Il server ha ricevuto:")
        print(loginRequest.username, loginRequest.password)
        
        data, repre = self.db.scanDb("utenti", ['username', 'password'], [loginRequest.username, loginRequest.password])
        dict = []
        
        # AGGIUNTAAAA
        if len(repre)!=0:
            dict.append(grpc_pb2.dictionary(key = "username", value=repre))
            dict.append(grpc_pb2.dictionary(key = "dummy", value="dummy"))
            response = grpc_pb2.session(dict = dict)
            return response
        if data == None:
            response = grpc_pb2.session(dict = [])
            return response
        if len(data)!= 0:
            result = data[0]
            dict.append(grpc_pb2.dictionary(key = "username", value=result['username']))
            dict.append(grpc_pb2.dictionary(key = "tipoUtente", value=str(result['tipoUtente'])))
            dict.append(grpc_pb2.dictionary(key = "email", value=result['email']))
    
        response = grpc_pb2.session(dict = dict)
        print("response", response)
        return response


    def insertAnUser(self, registrationRequest):
        """The function that performs the registration in dynamoDB 

        Args:
            registrationRequest (grpc_pb2.registrationRequest): GRPC auto-generated registrationRequest message. 
            It contains the credentials of the user

        Returns:
            BOOL,string: Return a Boolean in order to discriminate the success or failure of the insertion and an error message
        """
        try:
            id = uuid.uuid1()
            print(id)
            print('UUID per il nuovo account: ', str(id.time))
            print(registrationRequest.admin)
            username = registrationRequest.username

            put1 = self.db.putTransaction([['username','S',username],['password','S',registrationRequest.password],['tipoUtente','BOOL',registrationRequest.admin],
                ['email','S',registrationRequest.email]],'utenti')

            if registrationRequest.admin == True:

                put2 =  self.db.putTransaction ([['username','S',username],['nomeLido','S',registrationRequest.opt.beachClubName],
                ['luogo','S',registrationRequest.opt.location],
                ['ristorazione','BOOL',registrationRequest.opt.ristorazione],['bar','BOOL',registrationRequest.opt.bar],
                ['campi','BOOL',registrationRequest.opt.campi],['animazione','BOOL',registrationRequest.opt.animazione],
                ['palestra','BOOL',registrationRequest.opt.palestra]],'dettagliLido')

                response,msg = self.db.executeTransaction([put1,put2])

                if response == False:
                    return False, msg
                    
                paymentChannel = grpc.insecure_channel("{}:50055".format("localhost"))
                stubPayment = grpc_pb2_grpc.PaymentStub(paymentChannel)   

                response = stubPayment.insertCreditCard(grpc_pb2.creditDetails(username = registrationRequest.username,
                cardId = registrationRequest.opt.cardId, cvc = registrationRequest.opt.cvc,credito = 0))

                if response.operationResult == False:
                    print ("Undo previous write transaction...")
                    del1 = self.db.deleteTrasaction([['username','S',username]],'utenti')
                    del2 = self.db.deleteTrasaction([['username','S',username]],'dettagliLido')
                    response = self.db.executeTransaction([del1, del2])
                       
                    return False, "Registration has failed"
            else:

                response = self.db.executeTransaction([put1])     

                if response == False:
                    return False, msg
    
            result = self.sendEmail(registrationRequest.username, registrationRequest.email)  
        except grpc._channel._InactiveRpcError as e:
            print ("Undo previous write transaction...")
            del1 = self.db.deleteTrasaction([['username','S',username]],'utenti')
            del2 = self.db.deleteTrasaction([['username','S',username]],'dettagliLido')

            response,msg = self.db.executeTransaction([del1,del2])

            if (response == None):
                return False,  msg
                
            return False,  "Registration has failed"
                
        except Exception as e:
                print (repr(e))
                return False,  "Registration has failed"
        return True, "Registration has succeded"

    def configureBeachClub(self, configurationRequest, context):
        """ Change the actual beach club state

        Args:
            configurationRequest (grpc_pb2.configurationRequest): GRPC auto-generated configurationRequest message. 
            It contains the newest state for the beach club
            context (_type_): context information 

        Returns:
            grpc_pb2.response: GRPC auto-generated response message that tells if the registration has succeded and 
            a string that describes the state of the operation
        """
        
        print("Il server ha ricevuto:")
        print(configurationRequest.numRows, configurationRequest.numLettini, configurationRequest.numSdraio, 
            configurationRequest.numChair, configurationRequest.sessione.dict[0].value)
        numRows = configurationRequest.numRows
        for i in range(0, numRows):
                print("- Posti nella fila ", i, ": ", configurationRequest.array.numSeatInRow[i])

        result, errorMessage = self.insertNewestBeachClubConfig(configurationRequest)    
        response = grpc_pb2.response(operationResult = result, errorMessage = errorMessage)
        return response

    def insertNewestBeachClubConfig(self, configurationRequest):
        """ Function that performs the insertion in dynamoDB of the newest beach club state  

        Args:
            configurationRequest (grpc_pb2.configurationRequest): GRPC auto-generated configurationRequest message. 
            It contains the newest state for the beach club

        Returns:
            BOOL,string: Return a Boolean in order to discriminate the success or failure of the insertion and an error message
        """

            # Da riutilizzare ...
            #    delete = {'Delete': {'Key': {'lidoId': {'S': configurationRequest.username},'numeroFila': {'N': i+1}},'TableName': 'postazioniPerFila'}}
            #    put = {'Put':{'Item': {'lidoId': { 'S': username},'numeroFila': {'N':temp},'nOmbrelloni': {'N': seatByRows.numSeatInRow[i]}}, 'TableName': 'postazioniPerFila'}} 
        try:
            numRows = configurationRequest.numRows
            seatByRows = configurationRequest.array
            username = str(configurationRequest.sessione.dict[0].value)
            
            expressionAttributeValues = {}
            # ELIMINA TUTTE LE FILE PRECEDENTI: utile quando si cambia il numero di file
            data = self.db.scanDb("postazioniPerFila", ['lidoId'], [username])
            transactions = []
          
            for i in range (0,min(len(data),numRows)):

                update = self.db.updateTransaction ([['lidoId','S',username],['numeroFila','N',i+1]],[['nOmbrelloni','N',seatByRows.numSeatInRow[i]]],'postazioniPerFila')
               
                transactions.append(update)
            
            #Da aggiungere
            if len(data) < numRows:
                for i in range (len(data) , numRows):
                    put = self.db.putTransaction ([['lidoId','S',username],['numeroFila','N',i+1],['nOmbrelloni','N',seatByRows.numSeatInRow[i]]], 'postazioniPerFila')
                    
                    transactions.append(put)
            #Da rimuovere
            else :     
                for i in range (numRows , len(data)):
                    delete = self.db.deleteTrasaction ([['lidoId','S',username],['numeroFila','N',i+1]],'postazioniPerFila')
                  
                    transactions.append(delete)

            UpdateExpression= "SET totaleSdraio= :val1, totaleLettini = :val2, totaleSedie = :val3"
            update = self.db.updateTransaction([['username','S',username]],
            [['totaleSdraio','N',configurationRequest.numSdraio],['totaleLettini','N',configurationRequest.numLettini],['totaleSedie','N',configurationRequest.numChair]],'dettagliLido')
           
            transactions.append(update)
            print(transactions)

            response,msg = self.db.executeTransaction(transactions)
            if response == False:
                return False, msg 
            
        except Exception as e:
            print(repr(e))
            return False, "Insert operation has failed"
        return True, "Insert operation has succeded"
    
    def getAllBeachClubInCity (self, cityRequest, context):
        """ Obtain all the beach clubs in a particular city

        Args:
            cityRequest (grpc_pb2.cityRequest): GRPC auto-generated cityRequest message. 
            It Contains the city to search for
            context (_type_): _description_

        Returns:
            grpc_pb2.usernameResponse: GRPC auto-generated usernameResponse message that contains the beach clubs
        """
        city = cityRequest.city
        print('ho ricevuto la richiesta della ricerca di tutti i lidi nella città di {}'.format(city))

        data = self.db.scanDb('dettagliLido', ['luogo'], [city])
        if data == None:
            return  grpc_pb2.usernameResponse(usernameBeachClub=[])

        nomi_utente = []
        if(len(data)!=0):
            for i in range(0, len(data)):
                nomi_utente.append(data[i]['username'])
        response = grpc_pb2.usernameResponse(usernameBeachClub=nomi_utente)
        return response


    
    def getMatrix(self, request, context):
        """Return seats already occupied

        Args:
            request (grpc_pb2.reviewRequest): GRPC auto-generated message that contains the username of the beach club
            context (_type_): _description_

        Returns:
            grpc_pb2.matrix: Seats already occupied
        """
        lidoId = request.usernameBeachClub
        data = self.db.scanDb('postazioniPerFila', ['lidoId'], [lidoId])
        if data == None:
            return  grpc_pb2.usernameResponse(usernameBeachClub=[])
        numInRow = []
        if(len(data)!=0):
            for i in range(0, len(data)):
                numInRow.append(int(data[i]['nOmbrelloni']))
        response = grpc_pb2.matrix(numInRow=numInRow)
        return response

      
    def deleteAccount (self, deleteReq,context):
        """ Delete an active user account. It starts the SAGA pattern

        Args:
            deleteReq (grpc_pb2.deleteRequest): GRPC auto-generated message that contains intrinsics information in order to delete the account
            context (_type_): _description_

        Returns:
             GRPC auto-generated response message that tells if the delete op has succeded and a string that describes the function state
        """
        username = deleteReq.username
        try:

            self.establishConnectionSAGA()
            # pubblica un messaggio  per triggerare la delete
    
            request = "{}:{}".format (username,deleteReq.admin)
            print("SENDING A DELETE REQUEST")
            self.corr_id = str(uuid.uuid4())
          
            self.channelSAGA.basic_publish(
                exchange='', 
                routing_key= "Payment_request", 
                properties=pika.BasicProperties(
                        reply_to= "Account_request",
                    ),
                body=request
            ),

            self.connectionSAGA.process_data_events(time_limit=None)  
            print("END")
        except Exception as e:
            print(repr(e))
            return grpc_pb2.response(operationResult = False, errorMessage = "Delete has failed")

        response = grpc_pb2.response(operationResult = True, errorMessage = "Delete has succeded")
        return response


    def updateCredentials(self, updateReq, context):
        """Update the user's credentials 

        Args:
            updateReq (grpc_pb2.updateRequest): _description_
            context (_type_): _description_

        Returns:
            grpc_2.session: GRPC auto-generated message that contains newest credentials (if currectly updated) for that user
        """
        #dict = {"password" : updateReq.newPassword, "email": updateReq.newEmail}
        transactions = []
        try:
            if (updateReq.opt != None):
                print(updateReq.newPassword, updateReq.newEmail, updateReq.opt.beachClubName,
                updateReq.opt.location,updateReq.opt.cardId)
            else : 
                
                print( updateReq.newPassword, updateReq.newEmail)
                update = self.db.updateTransaction ([['username','S',updateReq.username]],[['password','S',updateReq.newPassword]],'utenti')
                
                transactions.append(update)   
        
            if (updateReq.admin == True):
                update = self.db.updateTransaction ([['username','S',updateReq.username]],
                [['nomeLido','S',updateReq.opt.beachClubName],['luogo','S',updateReq.opt.location],['cardId','S',updateReq.opt.cardId]],'dettagliLido')
                
                transactions.append(update) 

                print(update)

           
            response,msg =self.db.executeTransaction (transactions)

            if response == False:
                return grpc_pb2.session (dict = []) 

            list = []
            list.append(grpc_pb2.dictionary(key = "username", value=updateReq.username))
            list.append(grpc_pb2.dictionary(key = "tipoUtente", value= str(updateReq.admin)))
            list.append(grpc_pb2.dictionary(key = "email", value= updateReq.newEmail))
            response = grpc_pb2.session(dict = list)

        except Exception as e:
            print("non esistono campi da aggiornare nella tabella")
            print(repr(e))
            return grpc_pb2.session (dict = [])
      
        return response
    
    def establishConnection (self):
        """ Create a new instance of the Connection Object for RabbitMQ, then create a new channel and declares request and response queues
            for sending the email

        Returns:
            BOOL: return TRUE if the connection to RabbitMQ server has succeded
        """
        try :
            self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

            self.channel = self.connection.channel()

            #CODA PER TUTTE LE RICHIESTE
            result =self.channel.queue_declare(queue='emailQueue')
            self.requestQueue = result.method.queue

            #CODA PER LE RISPOSTE
            result =self.channel.queue_declare(queue='responseQueue:Accounting')
            self.responseQueue = result.method.queue

            #BINDING DELLA CODA delle risposte all'exchange con routing key pari ad Accounting
            self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
            self.channel.queue_bind(exchange='topic_logs', queue=self.responseQueue, routing_key="Accounting.*")

            #COSA FARE ALLA RISPOSTA???
            self.channel.basic_consume(
                queue=self.responseQueue,
                on_message_callback=self.onResponse,
                auto_ack=True)

        except Exception as e:
            print(repr(e))
            self.errorMsg = "Error in establishing connections and queues"
            return False
        return True

    def onResponse (self,ch,method,properties,body):
        """ Callback for the response message from the email service

        Args:
            ch (BlockingChannel): Instance of Blocking channel over which the communication is happening
            method (Delivery): meta information regarding the message delivery
            properties (BasicProperties): user-defined properties on the message
            body (string): body of the message
        """


        print("RESPONSE: %r:%r" % (method.routing_key, body))
        if self.connection != None and self.connection.is_open:
            self.connection.close()
    

    def sendEmail(self, username, email):
        """Send a request to the email service in order to start sending emails

        Args:
            username (string): user's username
            email (string): user's email

        Returns:
            BOOL,String: Return a Boolean in order to discriminate the success or failure of the function and an error message
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
                    correlation_id=self.corr_id,
                ),
                body=request)
            print("Send operation has succeded")
            self.connection.process_data_events(time_limit=None)
        except Exception as e:
            print(repr(e))
            return False , "Send operation has failed"
        return True, "Send operation has succeded"

    def getAllBeachClubUsername(self, emptyRequest, context):
        """return all the beach club's usernames in dynamoBD

        Args:
            emptyRequest (grpc_pb2.empty): GRPC auto-generated empty message
            context (_type_): _description_

        Returns:
            grpc_pb2.usernameBeachClub: List of beach club's username
        """
        
        print("ho ricevuto la richiesta di tutti i lidi")
        data = self.db.scanDb('utenti', ['tipoUtente'], [True])
        response = grpc_pb2.usernameResponse()
        for utente in data:
            print(utente)
            response.usernameBeachClub.append(utente['username'])
        return response
    
    
    
    def getBeachClubDetails(self, request, context):
        """Gets details of a beach club

        Args:
            request (grpc_pb2.reviewRequest): GRPC auto-generated request that contains the username for which to search for details
            context (_type_): _description_

        Returns:
            grpc_pb2.adminOptions: GRPC auto-generated response that contains the beach club's details
        """
        username = request.usernameBeachClub
        data = self.db.scanDb('dettagliLido',['username'], [username])
        
        if len(data) == 0:
            return None
        else:
            response = grpc_pb2.adminOptions(
                beachClubName=username,
                location=data[0]['luogo'],
                cardId=" ", 
                cvc=0, 
                ristorazione=data[0]['ristorazione'],
                bar=data[0]['bar'],
                campi=data[0]['campi'],
                animazione=data[0]['animazione'],
                palestra=data[0]['palestra']   
            )
        return response

def grpc_server (service):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_AccountingServicer_to_server(service, server)
    print('Starting ACCOUNTING SERVICE. Listening on port 50052.')
    server.add_insecure_port('[::]:50052')
    #server.add_insecure_port('172.24.0.3:50052')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

def sagaQueueConsumer(service):
    print(" [x] Awaiting SAGA requests")
    service.channelSAGA.start_consuming()
    
service = AccountingServicer()
x = threading.Thread(target=grpc_server, args=(service,))
x.start()


y = threading.Thread(target=sagaQueueConsumer,args=(service,))
y.start()
x.join()



