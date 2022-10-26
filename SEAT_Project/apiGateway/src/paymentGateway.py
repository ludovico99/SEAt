import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc

class PaymentGateway():

    def __init__(self):
        # self.paymentChannel = grpc.insecure_channel("{}:50055".format("localhost"))
        self.paymentChannel = grpc.insecure_channel("{}:50055".format("payment"))
        self.stubPayment = grpc_pb2_grpc.PaymentStub(self.paymentChannel)


    def listOfCards(self,lido_id,email,type):
        
        list = []
        list.append(grpc_pb2.dictionary(key = "username", value=lido_id))
        list.append(grpc_pb2.dictionary(key = "tipoUtente", value=type))
        list.append(grpc_pb2.dictionary(key = "email", value = email))
        sessione = grpc_pb2.session(dict = list)
        response = self.stubPayment.showCards(sessione)
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
        response = self.stubPayment.deleteCard(grpc_pb2.deleteCardRequest(username = lido_id, cardId = cardId))
        return True if response.operationResult == True else False

    def insertCreditCard(self,username, cardId, cvc, credito):

        if len(cardId) < 16: return False 
        elif len(cvc) < 3: return False
        elif int(credito) < 0: return False


        response = self.stubPayment.insertCreditCard(grpc_pb2.creditDetails(username =username,
            cardId = cardId, cvc = int(cvc),credito = credito))
        return True if response.operationResult == True else False