import os
import grpc
import time
from proto import grpc_pb2
from proto import grpc_pb2_grpc

class PaymentGateway():

    def __init__(self):
        
        self.rr = 0
        self.number_instances = int(os.environ['SCALE_FACTOR'])
        self.channels = []
        
        self.ch = grpc.insecure_channel("{}:50000".format("service_registry"))
        self.stubServiceRegistry = grpc_pb2_grpc.ServiceRegistryStub(self.ch)

        while (True):

            try:  
                response = self.stubServiceRegistry.getPortAndIp(grpc_pb2.registryRequest(serviceName= "PaymentServicer"))
                break
            except Exception as e:

                time.sleep(5)

        if response == None or response.responses[0].port == "0":
            print("{}:Unable to contact service registry: static binding needed to continue".format(self.__class__.__name__))
            for i in range (0, self.number_instances):
                tmp = i + 1 
                self.channels.append(grpc.insecure_channel("{}:{}".format("seat_project_payment_{}".format(tmp),"50055")))
                


        else :
            print("{}:Service registry successfully contacted: dynamic binding available".format(self.__class__.__name__))

            for i in range (0, len(response.responses)):
                self.channels.append(grpc.insecure_channel("{}:{}".format(response.responses[i].hostname,response.responses[i].port)))
            
            
        self.stubs = []
        for ch in self.channels:
            self.stubs.append(grpc_pb2_grpc.PaymentStub(ch))
        print("calling the start of the queue stuff")
        self.stubs[0].startConsume(grpc_pb2.empty())
        

    def listOfCards(self,lido_id,email,type):
        """entry point for the retrieve of the cards associated to the user

        Args:
            lido_id (String): username
            email (String): email
            type (BOOL): type of user, TRUE if is admin

        Returns:
            LIst: list of cards with details
        """
        
        list = []
        list.append(grpc_pb2.dictionary(key = "username", value=lido_id))
        list.append(grpc_pb2.dictionary(key = "tipoUtente", value=type))
        list.append(grpc_pb2.dictionary(key = "email", value = email))
        sessione = grpc_pb2.session(dict = list)
        
        # response = self.stubPayment.showCards(sessione)
        print("Richiesta a {}".format(self.rr))
        response = self.stubs[self.rr].showCards(sessione)
        self.rr = (self.rr + 1)%int(self.number_instances)
        cards = []
        for i in response.cards:
            card = []
            card.append(i.cardId)
            card.append(i.credito)
            card.append(i.cvc)
            card.append(i.id)
            cards.append(card)
        return cards

    def deleteCard (self,lido_id, cardId): 
        """entry point for card removal

        Args:
            lido_id (String): username of the card's owner
            cardId (String): card identifier

        Returns:
            BOOL: outcome of the operation
        """
        # response = self.stubPayment.deleteCard(grpc_pb2.deleteCardRequest(username = lido_id, cardId = cardId))
        response = self.stubs[0].deleteCard(grpc_pb2.deleteCardRequest(username = lido_id, cardId = cardId))
        return True if response.operationResult == True else False

    def insertCreditCard(self,username, cardId, cvc, credito):
        """entry point for the insertion of a new payment card. If the card exists the function modify the existing one.

        Args:
            username (String): username of the card's owner
            cardId (String): card identifier
            cvc (String): card's cvc
            credito (int): amount of money to add in the card

        Returns:
            _type_: _description_
        """

        if len(cardId) < 16: return False 
        elif len(cvc) < 3: return False
        elif int(credito) < 0: return False


        # response = self.stubPayment.insertCreditCard(grpc_pb2.creditDetails(username =username,
        response = self.stubs[0].insertCreditCard(grpc_pb2.creditDetails(username =username,
            cardId = cardId, cvc = int(cvc),credito = credito))
        return True if response.operationResult == True else False