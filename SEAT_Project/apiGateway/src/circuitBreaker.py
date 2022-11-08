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



    

    def onGetSuggestionOpen (self,param):
        suggestions = None
        print("[CB] CIRCUITO APERTO")
        msg = "GetSuggestions al momento non disponibile"
        print(msg)
        return suggestions, msg

    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onGetSuggestionOpen)
    def getSuggestions(self,proposalRequest):
        print("[CB] sto chiamando il microservizio")
        response = self.stubReservation.getListOfProposal(proposalRequest)
        suggestions = []
        for offerta in response.offerta:
            proposta = [offerta.lido_id, offerta.city, round(int(offerta.distance), 2), offerta.price, round(int(offerta.averageReview),2), offerta.index]
            suggestions.insert(offerta.index, proposta)
        return suggestions, ""

    

    def onGetReservedSeatOpen (self,param):
        reservations = None
        print("[CB] CIRCUITO APERTO")
        msg = "GetReservedSeats al momento non disponibile"
        print(msg)
        return reservations, msg

    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onGetReservedSeatOpen)
    def getReservedSeats(self, request):
        print("[CB] sto chiamando il microservizio")
        response = self.stubReservation.getReservedSeats(request)
        return response.reservation, ""


    
    def onReserveOpen(self, param):
        operationResult = False
        print("[CB] CIRCUITO APERTO")
        msg = "Reserve al momento non disponibile"
        print(msg)
        return operationResult, msg

    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onReserveOpen)
    def reserve(self, request):
        print("[CB] sto chiamando il microservizio")
        response = self.stubReservation.reserve(request)
        return response.operationResult, response.errorMessage

    
    
    def onManualReserveOpen(self, param):
        operationResult = False
        print("[CB] CIRCUITO APERTO")
        msg = "manualReserve al momento non disponibile"
        print(msg)
        return operationResult, msg

    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onManualReserveOpen)
    def manualReserve(self, request):
        print("[CB] sto chiamando il microservizio")
        response = self.stubReservation.manualReserve(request)
        return response.operationResult, response.errorMessage



    
    # CB SULLE CONNESSIONI ---------------------------------------------------------------------------------------------------------------

    def onConnectionNotEstablished(self):
        suggestions = None
        print("[CB] CIRCUITO APERTO")
        msg = "Impossibile stabilire la connessione con il microservizio richiesto"
        print(msg)
        return suggestions, msg  

    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToReservationService(self):
        self.reservationChannel = grpc.insecure_channel("{}:50051".format("reservation"))
        self.stubReservation = grpc_pb2_grpc.ReservationStub(self.reservationChannel)


    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onConnectionNotEstablished)
    def tryConnectionToAccountingService(self):
        self.accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
        self.stubAccounting=grpc_pb2_grpc.AccountingStub(self.accountingChannel)



    # CB SU ALCUNE OPERAZIONI DI LOGIN -------------------------------------------------------------------------------------------------

    def onLoginFailed(self,param1,param2):
        print("[CB] CIRCUITO APERTO")
        print("Login al momento non disponibile")
        return grpc_pb2.sessione(dict=[])



    def onGetMatrixFailed(self,param1):
        print("[CB] CIRCUITO APERTO")
        print("GetMatrix al momento non disponibile")
        return grpc_pb2.matrix(numInRow=[])



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onLoginFailed)
    def login(self, username,password):
        print("[CB] sto chiamando il microservizio Accounting")
        return self.stubAccounting.login(grpc_pb2.loginRequest(username=username, password=password))



    @circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onGetMatrixFailed)
    def getMatrix(self,username):
        print("[CB] sto chiamando il microservizio Accounting")
        return self.stubAccounting.getMatrix(grpc_pb2.reviewRequest(usernameBeachClub = username))