import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc

class QuoteGateway():

    def __init__(self):
       self.quoteChannel = grpc.insecure_channel("{}:50053".format("localhost"))
       self.stubQuote = grpc_pb2_grpc.QuoteStub(self.quoteChannel)

    def modifyPrice(self,priceOmbrellone, priceSdraio, priceLettino, priceSedia, incrPrimeFile, incrAltaStagione, incrBassaStagione, incrMediaStagione, username):
        
        response = self.stubQuote.insertPrices(grpc_pb2.priceRequest(priceOmbrellone = priceOmbrellone,
            priceSdraio= priceSdraio,priceLettino = priceLettino, priceSedia = priceSedia, incrPrimeFile = incrPrimeFile,
            incrAltaStagione = incrAltaStagione, incrBassaStagione= incrBassaStagione, incrMediaStagione = incrMediaStagione,
            username = username))