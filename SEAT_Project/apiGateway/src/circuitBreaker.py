from circuitbreaker import circuit
import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc


def onCircuitOpen():

    suggestions = None
    print("[CB] CIRCUITO APERTO")
    msg = "funzionalità richiesta al momento non disponibile"
    return suggestions, msg


@circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onCircuitOpen)
def getSuggestions(stubReservation, inputParam):

    print("[CB] sto chiamando il microservizio")
    response = stubReservation.getListOfProposal(inputParam)
    suggestions = []
    for offerta in response.offerta:
        proposta = [offerta.lido_id, offerta.city, round(int(offerta.distance), 2), offerta.price, round(int(offerta.averageReview),2), offerta.index]
        suggestions.insert(offerta.index, proposta)
    return suggestions, ""

@circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onCircuitOpen)
def tryConnectToAccountingService():
    accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
    return grpc_pb2_grpc.AccountingStub(accountingChannel)   
   
   