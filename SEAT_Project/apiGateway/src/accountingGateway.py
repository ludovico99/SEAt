import time
import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc
import re
import circuitBreaker

def isValid(email):
    """_ Auxiliary function that check if the email inserted is valid or not

    Args:
        email (string): String that respresents the email

    Returns:
        BOOL: Returns True if the email is valid otherwise returns False
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        print("Valid email")
        return True
    else:
        print("Invalid email")
        return False

class AccountingGateway():
    """
    AccountingGateway is the entry point for the interactions with the accounting service
    """
    def __init__(self):
        self.cb = circuitBreaker.MyCircuitBreaker(self.__class__.__name__) #only for the login method invocation
        self.ch = grpc.insecure_channel("{}:50000".format("service_registry"))
        self.stubServiceRegistry = grpc_pb2_grpc.ServiceRegistryStub(self.ch) 
        while (True):
            try:  
                response = self.stubServiceRegistry.getPortAndIp(grpc_pb2.registryRequest(serviceName= "AccountingServicer"))
                break
            except Exception as e:
                time.sleep(5)

        if response == None or response.responses[0].port == "0":
            print("{}:Unable to contact service registry: static binding needed to continue".format(self.__class__.__name__))
            self.channelAccounting = grpc.insecure_channel("{}:{}".format("accounting","50052"))
            self.stubAccounting = grpc_pb2_grpc.AccountingStub(self.channelAccounting) 


        else :
            print("{}:Service registry successfully contacted: dynamic binding available".format(self.__class__.__name__))
            self.channelAccounting = grpc.insecure_channel("{}:{}".format(response.responses[0].hostname,response.responses[0].port))
            self.stubAccounting = grpc_pb2_grpc.AccountingStub(self.channelAccounting) 

 
    
    def changeConfiguration(self,numRows, numLettini, numSdraio, numChair, postiPerFila, username, tipoUtente, email):
        """Entry point for the change configuration operation

        Args:
            numRows (int): number of rows to insert
            numLettini (int): number of sunbeds to insert
            numSdraio (int): number of deckchair to insert
            numChair (int): number of chair to insert
            postiPerFila (_type_): _description_
            username (string): username of the user
            tipoUtente (bool): True if the user is a beach club owner otherwise False
            email (string): email of the user

        Returns:
            BOOL,String: Returns True if the operation has succeded. The result is associated with a string that explains the final state of the operation
        """
        
        if numRows < 0:
            return False, "number of rows is less than 0"
        if numSdraio < 0:
            return False, "number of deckchairs is less than 0"
        if numChair < 0:
            return False, "number of chair is less than 0"
        if numLettini < 0:
            return False, "number of sunbeds is less than 0"

        numSeatByRow = grpc_pb2.numSeatByRow()
        for j in range(0, numRows):
            numSeatByRow.numSeatInRow.append(postiPerFila[j])
        list = []
        list.append(grpc_pb2.dictionary(key = "username", value=username))
        list.append(grpc_pb2.dictionary(key = "tipoUtente", value=tipoUtente))
        list.append(grpc_pb2.dictionary(key = "email", value=email))
        sessione = grpc_pb2.session(dict = list)
                    
                        
        response = self.stubAccounting.configureBeachClub(grpc_pb2.configurationRequest(
            numRows=numRows, 
            array=numSeatByRow,
            numLettini=numLettini,
            numSdraio=numSdraio,
            numChair=numChair,
            sessione=sessione
        ))

        if response.operationResult == True:
            return True, "BeachClub config has been changed correctly" 
        else:
            return False, "An Error has occurred" 
        

    def changeAccountCredentials(self,isAdmin, new_password, new_email, new_name, new_place, new_card,new_cvc, username):
        """ Entry point for the change account credentials operation

        Args:
            isAdmin (BOOL): True if the user is a beach club owner otherwise False
            new_password (string): new password to insert
            new_email (string): new email to insert
            new_name (string): new name to insert
            new_place (string): new place to insert
            new_card (string): new cardId to insert
            username (string): Actual username 

        Returns:
            BOOL,String: Returns True if the operation has succeded. The result is associated with a string that explains the final state of the operation
        """
        try:
            if len(new_email) > 0 and isValid(new_email) == False:
                return False, "Email inserted is not valid"

            if new_card != None and len(new_card) != 0 and (not str(new_card).isnumeric() or len(new_card) != 16):
                return False, "Card id inserted is not valid"

            if new_cvc != None and len(new_cvc) != 0 and (not str(new_cvc).isnumeric() or len(new_cvc) != 3):
                return False, "CVC inserted is not valid"

            if isAdmin == True:
                opt = grpc_pb2.adminOptions(beachClubName = new_name, location=new_place , cardId = new_card, cvc = new_cvc)
            else:
                opt = None
            response = self.stubAccounting.updateCredentials(grpc_pb2.updateRequest(
                username = username,
                newPassword= new_password , 
                newEmail = new_email,
                admin = isAdmin,
                opt = opt ))
            if len(response.dict) == 0:
                return False, "An error has occurred"
            return True, "Your Account credentials have been correctly changed"
        
        except Exception as e:
            print(repr(e))
            return False, "An error has occurred"
    

    def deleteAccount(self,username, admin):
        """Entry point for deleteAccount operation

        Args:
            username (string): Username of the account that is pointed out to be deleted
            isAdmin (bool): True if the user is a beach club owner otherwise False

        Returns:
            Bool: Returns True if the operation has succeded
        """
        response = self.stubAccounting.deleteAccount(grpc_pb2.deleteRequest(username = username, admin = admin))
        if response == None: 
            print ("Delete operation has failed")
            result = False
        else: 
            result = True
        return result

    def newAccount(self,username, password, email, admin, beachClubName, location, cardId,cvc, details):
        """ Entry point for the newAccount operation

        Args:
            username (string): username of the account to be created
            password (string): password or the account to be created
            email (string): email of the account to be created
            admin (bool): True if the user is a beach club owner otherwise False
            beachClubName (string): beach club name of the account to be created
            location (string): location of the beach club related to (if admin is True)
            cardId (string): cardId of the user to be created
            cvc (string): cvc associated with the cardId
            details (string): beach club's details

        Returns:
            Bool,string: Returns True if the operation has succeded. The result is associated with a string that explains the final state of the operation
        """
        try:
            if isValid(email) == False:
                return False, "Email inserted is not valid"

            if admin == True:
                if not str(cardId).isnumeric() or len(cardId) != 16:
                    return False, "CardId inserted is not valid"
                
                if not str(cvc).isnumeric() or len(cvc) != 3:
                     return False, "CVC inserted is not valid"
            
            adminOptions = grpc_pb2.adminOptions(
                beachClubName=beachClubName, 
                location=location, 
                cardId=cardId,
                cvc = cvc,
                ristorazione=details[0], 
                bar=details[1], 
                campi=details[2], 
                animazione=details[3], 
                palestra=details[4]
            )
            
            response = self.stubAccounting.registerAccount(grpc_pb2.registrationRequest(
            username=username, password=password, email=email, admin=admin, opt=adminOptions))
 
            return bool(response.operationResult), str(response.errorMessage)

        except Exception as e:
            print(repr(e))
            return False, "An error has occurred"
       
    def login (self,username, password):
        """Entry point for the login operation

        Args:
            username (string): username of the user who is logging in
            password (string): password of the user who is logging in

        Returns:
            dict,list: Returns a dict containing the session stats and a list containing a matrix that represents the actual state of its seats (if the user is an admin)
        """
        try:
            mySession = {}
            matrix = []
            sessione = self.cb.login(username,password)
            
            #La logica di gestione della connessione ?? gestita da grpc, se ho un errore durante l'invocazione del metodo ?? gRPC che lo gestisce. Il compito
            #del circuit breaker ?? quello di creare una connessione con il microservizio se possibile
            if len(sessione.dict) == 0:
                return {},[]
                
            mySession['username'] = sessione.dict[0].value
            mySession['tipoUtente'] = sessione.dict[1].value
            mySession['email'] = sessione.dict[2].value

            if sessione.dict[1].value == "True":
                response = self.cb.getMatrix(username)
                for i in response.numInRow:
                    matrix.append(i)
                    
            return mySession,matrix

        except Exception as e:
            print(repr(e))
            return {},[]