from circuitbreaker import circuit
from circuitbreaker import CircuitBreaker
import grpc
import accountingGateway
import paymentGateway
import reservationGateway
import quoteGateway
import reviewGateway
from proto import grpc_pb2
from proto import grpc_pb2_grpc


class MyCircuitBreaker(CircuitBreaker):

    def __init__(self, className):
        if className == accountingGateway.AccountingGateway.__name__:
            self.tryConnectionToAccountingService()
        if className == reservationGateway.ReservationGateway.__name__:
            self.tryConnectionToReservationService()
        if className == quoteGateway.QuoteGateway.__name__:
            self.tryConnectionToQuoteService()
        if className == paymentGateway.PaymentGateway.__name__:
            self.tryConnectionToPaymentService()
        if className == reviewGateway.ReviewGateway.__name__:
            self.tryConnectionToReviewService()


    def onLoginFailed(self,param1,param2):
        print("[CB] CIRCUITO APERTO")
        print("Login al momento non disponibile")
        return grpc_pb2.sessione(dict=[])



    def onGetMatrixFailed(self,param1):
        print("[CB] CIRCUITO APERTO")
        print("GetMatrix al momento non disponibile")
        return grpc_pb2.matrix(numInRow=[])

    def onConnectionNotEstablished(self):
        suggestions = None
        print("[CB] CIRCUITO APERTO")
        msg = "Impossibile stabilire la connessione con il microservizio richiesto"
        print(msg)
        return suggestions, msg  


    def onGetSuggestionOpen (self,param):
        suggestions = None
        print("[CB] CIRCUITO APERTO")
        msg = "GetSuggestions al momento non disponibile"
        print(msg)
        return suggestions, msg
    
        
    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onGetSuggestionOpen)
    def getSuggestions(self,inputParam):
        print("[CB] sto chiamando il microservizio")
        response = self.stubReservation.getListOfProposal(inputParam)
        suggestions = []
        for offerta in response.offerta:
            proposta = [offerta.lido_id, offerta.city, round(int(offerta.distance), 2), offerta.price, round(int(offerta.averageReview),2), offerta.index]
            suggestions.insert(offerta.index, proposta)
        return suggestions, ""



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onLoginFailed)
    def login(self, username,password):
        print("[CB] sto chiamando il microservizio Accounting")
        return self.stubAccounting.login(grpc_pb2.loginRequest(username=username, password=password))



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onGetMatrixFailed)
    def getMatrix(self,username):
        print("[CB] sto chiamando il microservizio Accounting")
        return self.stubAccounting.getMatrix(grpc_pb2.reviewRequest(usernameBeachClub = username))


    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToAccountingService(self):
        self.accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
        self.stubAccounting=grpc_pb2_grpc.AccountingStub(self.accountingChannel)



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToReservationService(self):
        self.reservationChannel = grpc.insecure_channel("{}:50051".format("reservation"))
        self.stubReservation = grpc_pb2_grpc.ReservationStub(self.reservationChannel)



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToQuoteService(self):
        self.quoteChannel = grpc.insecure_channel("{}:50053".format("quote"))
        self.stubQuote = grpc_pb2_grpc.QuoteStub(self.quoteChannel)



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToReviewService(self):
        self.reviewChannel = grpc.insecure_channel("{}:50054".format("review"))
        self.stubReview = grpc_pb2_grpc.ReviewStub(self.reviewChannel)



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToPaymentService(self):
        self.paymentChannel = grpc.insecure_channel("{}:50055".format("payment"))
        self.stubPayment = grpc_pb2_grpc.PaymentStub(self.paymentChannel) 