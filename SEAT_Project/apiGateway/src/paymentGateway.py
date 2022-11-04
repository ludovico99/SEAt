import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc

class PaymentGateway():

    def __init__(self):
        self.paymentChannel = grpc.insecure_channel("{}:50055".format("payment"))
        self.stubPayment = grpc_pb2_grpc.PaymentStub(self.paymentChannel)


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
        """entry point for card removal

        Args:
            lido_id (String): username of the card's owner
            cardId (String): card identifier

        Returns:
            BOOL: outcome of the operation
        """
        response = self.stubPayment.deleteCard(grpc_pb2.deleteCardRequest(username = lido_id, cardId = cardId))
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


        response = self.stubPayment.insertCreditCard(grpc_pb2.creditDetails(username =username,
            cardId = cardId, cvc = int(cvc),credito = credito))
        return True if response.operationResult == True else False