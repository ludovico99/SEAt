import grpc
import time
from proto import grpc_pb2
from proto import grpc_pb2_grpc

class QuoteGateway():

    def __init__(self):
        self.ch = grpc.insecure_channel("{}:50057".format("service_registry"))
        self.stubServiceRegistry = grpc_pb2_grpc.ServiceRegistryStub(self.ch) 
        while (True):
            try:  
                response = self.stubServiceRegistry.getPortAndIp(grpc_pb2.registryRequest(serviceName= "QuotesServicer"))
                break
            except Exception as e:

                time.sleep(5)

        if response.responses[0].port == "0":
            print("{}:Unable to contact service registry: static binding needed to continue".format(self.__class__.__name__))
            self.quoteChannel = grpc.insecure_channel("{}:{}".format("quote","50053"))
            self.stubQuote = grpc_pb2_grpc.QuoteStub(self.quoteChannel) 


        else :
            print("{}:Service registry successfully contacted: dynamic binding available".format(self.__class__.__name__))
            self.quoteChannel = grpc.insecure_channel("{}:{}".format(response.responses[0].hostname,response.responses[0].port))
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