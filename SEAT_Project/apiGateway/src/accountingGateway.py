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
        self.accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
        self.stubAccounting = grpc_pb2_grpc.AccountingStub(self.accountingChannel)   
    
    def changeConfiguration(self,numRows, numLettini, numSdraio, numChair, postiPerFila, username, tipoUtente, email):
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
        

    def changeAccountCredentials(self,isAdmin, new_password, new_email, new_name, new_place, new_card, username, old_email):
        """ Entry point for the change account credentials operation

        Args:
            isAdmin (BOOL): True if the user is a beach club owner otherwise False
            new_password (string): newest password to insert
            new_email (string): newest email to insert
            new_name (string): newest name to insert
            new_place (string): newest place to insert
            new_card (string): newest cardId to inser
            username (string): Actual username 
            old_email (string): Actual email

        Returns:
            BOOL,String: Returns True if the operation has succeded. The result is associated with a string that explains the final state of the operation
        """
        try:
            if isValid(new_email) == False:
                return False, "Email inserted is not valid"

            if isAdmin == True:
                opt = grpc_pb2.adminOptions(beachClubName = new_name, location=new_place , cardId = new_card)
            else:
                opt = None
            response = self.stubAccounting.updateCredentials(grpc_pb2.updateRequest(
                username = username,
                newPassword= new_password , 
                newEmail = new_email if new_email != "" else old_email,
                admin = isAdmin,
                opt = opt ))
            if len(response) == 0:
                return False, "An error has occurred"
            return True, "Your Account credentials have been correctly changed" if response.operationResult == True else False, "Error has been occurred trying to update credentials"
        
        except Exception as e:
            print(repr(e))
            return False, "An error has occurred"
    

    def deleteAccount(self,username, isAdmin):
        """Entry point for deleteAccount operation

        Args:
            username (string): Username of the account that is pointed out to be deleted
            isAdmin (bool): True if the user is a beach club owner otherwise False

        Returns:
            Bool: Returns True if the operation has succeded
        """
        response = self.stubAccounting.deleteAccount(grpc_pb2.deleteRequest(username = username, admin = isAdmin))
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
                if len(cardId) < 16:
                    return False, "CardId inserted is not valid"
                
                if len(cvc) < 3:
                     return False, "CVC inserted is not valid"
            
            adminOptions = grpc_pb2.adminOptions(
                beachClubName=beachClubName, 
                location=location, 
                cardId=cardId,
                cvc = int(cvc) ,
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
            username (string): _description_
            password (string): _description_

        Returns:
            dict,list: Returns a dict containing the session stats and a list containing a matrix that represents the actual state of its seats (if the user is an admin)
        """
        try:
            mySession = {}
            matrix = []

            stub = circuitBreaker.tryConnectToAccountingService()
            sessione = stub.login(grpc_pb2.loginRequest(username=username, password=password))
            #La logica di gestione della connessione è gestita da grpc, se ho un errore durante l'invocazione del metodo è gRPC che lo gestisce. Il compito 
            #del circuit breaker è quello di creare una connessione con il microservizio se possibile

            mySession['username'] = sessione.dict[0].value
            mySession['tipoUtente'] = sessione.dict[1].value
            mySession['email'] = sessione.dict[2].value

            if sessione.dict[1].value == "True":
                
                response = self.stubAccounting.getMatrix(grpc_pb2.reviewRequest(usernameBeachClub = username))
                
                for i in response.numInRow:
                    matrix.append(i)
                    
            return mySession,matrix

        except Exception as e:
            print(repr(e))
            return {},[]
         