from concurrent import futures
import threading
import time
import grpc
import uuid
import pika
import boto3
from dBUtils import DBUtils
import os
from functools import partial
from connectionEmail import ConnectionEmail
from connectionSaga import ConnectionSaga
import socket

from proto import grpc_pb2
from proto import grpc_pb2_grpc


class AccountingServicer(grpc_pb2_grpc.AccountingServicer):
    
    def __init__(self):
        """Costructor for Accounting service class
        """
        self.db = DBUtils()
        self.port = "50052"
        result = self.notifyServiceRegistry(self.port)
        if result == False:
            print("The notification to the service registry has failed. The Accounting service should be unavailable")

        

    def notifyServiceRegistry (self,port):
        """Send a notification about its port number

        Args:
            port (string): port number of the accounting service

        Returns:
            BOOL: Return True if the message has been sent correctly
        """
        
        try:
            queue_name = "service_registry_queue"
            sqs = boto3.client('sqs',region_name='us-east-1')
            hostname = socket.gethostname()
            ipAddr = socket.gethostbyname(hostname)
            response = sqs.send_message(
            QueueUrl= queue_name,
            DelaySeconds=10,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'Accounting service notification'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'Accounting service'
                },
                
            },
            MessageBody=(
                "My port number is :{}, my ipAddress is :{}, service name :{}, hostname :{}.".format(port, ipAddr, self.__class__.__name__, hostname)
            )
        )

            #print(response['MessageId'])
            return True

        except Exception as e:
            print(repr(e))
            return False


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
        
        data = self.db.scanDb("utenti", ['username', 'password'], [loginRequest.username, loginRequest.password])
        dict = []
            
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
                    
                paymentChannel = grpc.insecure_channel("{}:50055".format("payment"))
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
    
            # result = self.sendEmail(registrationRequest.username, registrationRequest.email)
            connessione = ConnectionEmail()
            result, errorMsg = connessione.sendEmail (registrationRequest.username, registrationRequest.email)
            print ("result:{}, ErrorMsg:{}".format(result, errorMsg))  
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

            connessione = ConnectionSaga()
            result, errorMsg = connessione.deleteAccount(username,deleteReq.admin)
            if result == False:
                return  grpc_pb2.response(operationResult = False, errorMessage=errorMsg) 
            
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
        transactions = []
        aux = []
        try:
            username = updateReq.username
            password = updateReq.newPassword
            email = updateReq.newEmail
            if updateReq.opt == None and updateReq.admin == True:
                return grpc_pb2.session (dict = [])


            if (updateReq.opt != None):
                print(updateReq.newPassword, updateReq.newEmail, updateReq.opt.beachClubName,
                updateReq.opt.location,updateReq.opt.cardId, updateReq.opt.cvc)

            else : 
                print(updateReq.newPassword, updateReq.newEmail)


            if len (password) > 0:
                aux.append(['password','S',password])  
            if  len (email) > 0:
                aux.append(['email','S',email])
            if len(aux) > 0:
                update = self.db.updateTransaction ([['username','S',username]],aux,'utenti')
                transactions.append(update) 

            if updateReq.opt != None and updateReq.admin == True:
                beachClub = updateReq.opt.beachClubName
                location = updateReq.opt.location
                cardId = updateReq.opt.cardId
                cvc = updateReq.opt.cvc
                aux = []
                    
                if len(beachClub) > 0:
                    aux.append(['nomeLido','S',beachClub])
                if len(location) > 0:
                    aux.append(['luogo','S',location])

                if len (aux) > 0:
                    update = self.db.updateTransaction ([['username','S',updateReq.username]],aux,'dettagliLido')
                    transactions.append(update) 

            print(transactions)
            if len(transactions) > 0:        
                response,msg =self.db.executeTransaction (transactions)
                if response == False:
                    return grpc_pb2.session (dict = [])

            if updateReq.opt != None and updateReq.admin == True:
                paymentChannel = grpc.insecure_channel("{}:50055".format("payment"))
                stubPayment = grpc_pb2_grpc.PaymentStub(paymentChannel)   

                if len(cardId) > 0 and len(cvc)>0:
                    response = stubPayment.insertCreditCard(grpc_pb2.creditDetails(username = username,
                    cardId = cardId, cvc = cvc,credito = 0)) 

            list = []
            list.append(grpc_pb2.dictionary(key = "username", value=username))
            list.append(grpc_pb2.dictionary(key = "tipoUtente", value= str(updateReq.admin)))
            list.append(grpc_pb2.dictionary(key = "email", value= email))
            response = grpc_pb2.session(dict = list)

        except Exception as e:
            print(repr(e))
            return grpc_pb2.session (dict = [])
      
        return response
    
    
    
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

service = AccountingServicer()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_AccountingServicer_to_server(service, server)
print('Starting ACCOUNTING SERVICE. Listening on port {}.'.format(service.port))
server.add_insecure_port('[::]:{}'.format(service.port))
server.start()
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)



