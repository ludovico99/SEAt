import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc

class QuoteGateway():

    def __init__(self):
        self.quoteChannel = grpc.insecure_channel("{}:50053".format("quote"))
        self.stubQuote = grpc_pb2_grpc.QuoteStub(self.quoteChannel)

    def modifyPrice(self,priceOmbrellone, priceSdraio, priceLettino, priceSedia, incrPrimeFile, incrAltaStagione, incrBassaStagione, incrMediaStagione, username):
        """_entry point to modify prices of the beach club that are seen by users

        Args:
            priceOmbrellone (int): new price for the seat (umbrella)
            priceSdraio (int): new price for the deckchair
            priceLettino (int): new price for the beach lounger
            priceSedia (int): new price for the chair
            incrPrimeFile (int): new price for the FIRST ROW increment
            incrAltaStagione (int): new price for the HIGH SEASON increment
            incrBassaStagione (int): new price for the LOW SEASON increment
            incrMediaStagione (int): new price for the MEDIUM SEASON increment
            username (String): username of the beach club
        """
        
        response = self.stubQuote.insertPrices(grpc_pb2.priceRequest(priceOmbrellone = priceOmbrellone,
            priceSdraio= priceSdraio,priceLettino = priceLettino, priceSedia = priceSedia, incrPrimeFile = incrPrimeFile,
            incrAltaStagione = incrAltaStagione, incrBassaStagione= incrBassaStagione, incrMediaStagione = incrMediaStagione,
            username = username))