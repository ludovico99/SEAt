from concurrent import futures
from datetime import datetime
import time
import grpc

from dBUtils import DBUtils
from quoteLogic import QuoteLogic

from proto import grpc_pb2
from proto import grpc_pb2_grpc

class QuotesServicer(grpc_pb2_grpc.QuoteServicer):
    
    def __init__(self):
        self.errorMsg = ""
        # self.iPAddress = "localhost"  

        self.db = DBUtils()
        self.logic = QuoteLogic()


    def computeQuotes(self, quoteForm, context):            # Nuova versione  
        """ compute the price for the requested beach club

        Args:
            grpc_pb2.quoteForm (quoteForm): grpc message with the details to compute the price
            context (_type_): 

        Returns:
            grpc_pb2.quoteResponse: grpc message with the beach club username and the computed price
        """

        quotes = []

        # 1. calcolare in che stagioni cadono le date selezionate per la prenotazione 
        #    (e quanti giorni vanno prenotati in ognuna)

        fromDate = datetime.fromtimestamp(quoteForm.fromDate.seconds + quoteForm.fromDate.nanos/1e9)
        toDate = datetime.fromtimestamp(quoteForm.toDate.seconds + quoteForm.toDate.nanos/1e9)
        stagioni = self.logic.dayInEachSeason(fromDate, toDate)

        if stagioni == None:
            response = grpc_pb2.quoteResponse(quotes = quotes)
            return response
        
        # 2. prendere tutti i prezzi disponibili

        # response = self.pricePerPiece.scan()
        # row_data = response['Items']
        # while 'LastEvaluatedKey' in response:
        #     response = self.pricePerPiece.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        #     row_data.extend(response['Items'])  

        response = self.db.scanDb ('pricePerPiece',[],[])

        if response == None:
         return  grpc_pb2.quoteResponse(quotes = grpc_pb2.quote())

        prezzi = {}  # {lido: {pezzo:costo, ...}}  

        for item in response:
            prezzi_lido = {}
            prezzi_lido.update({item['pezzo']:int(item['costo'])})
            if len(prezzi_lido) == 0:
                continue
            elif item['lidoId'] not in prezzi.keys():
                prezzi[item['lidoId']] = prezzi_lido 
            else:
                prezzi[item['lidoId']].update(prezzi_lido)

        for lido_id in prezzi:
            
            # 3. calcolare il costo giornaliero
            
            print("[", lido_id,"]")

            prezzo_giornaliero = (prezzi[lido_id]['lettino']*quoteForm.numLettini)+(prezzi[lido_id]['ombrellone']*quoteForm.numUmbrella)+ (prezzi[lido_id]['sdraio']*quoteForm.numSdraio)+ (prezzi[lido_id]['sedia']*quoteForm.numChair)
            print("  prezzo standard = ", prezzi[lido_id]['lettino'],"*",quoteForm.numLettini,"+",prezzi[lido_id]['ombrellone'],"*",quoteForm.numUmbrella,"+",
            prezzi[lido_id]['sdraio'],"*",quoteForm.numSdraio,"+",prezzi[lido_id]['sedia'],"*",quoteForm.numChair,"= ", prezzo_giornaliero)

            # 4. cercare l'incremento sulla fila desiderata

            numRow = str(quoteForm.numRow)            
            incremento_fila = 0
            data = self.db.scanDb('pricePerRow', ['lidoId', 'row'], [lido_id, numRow])
            if len(data) != 0:
                incremento_fila = data[0]['incr']

            # incremento_fila = self.lookUpIncreaseInDb(lido_id, attrValue)
            print("  incremento fila: ", prezzo_giornaliero,"+", incremento_fila,"=", prezzo_giornaliero+int(incremento_fila))
            prezzo_giornaliero = prezzo_giornaliero + int(incremento_fila)

            # 5. cercare l'incremento sul periodo desiderato
            
            prezzo_totale = 0
            for s in stagioni:
                if s=='1':
                    value = "incrBassaStagione"
                elif s=='2':
                    value = "incrMediaStagione"
                else:
                    value = "incrAltaStagione"
            
                attrValue = {}
                attrValue.update({'key':'season'})
                attrValue.update({'value': value })
                
                incremento_stagione = 0
                data2 = self.db.scanDb('pricePerSeason', ['lidoId', 'season'], [lido_id, value])
                if len(data2) != 0:
                    incremento_stagione = data2[0]['incr']
                # incremento_stagione = self.lookUpIncreaseInDb(lido_id, attrValue)
                print("  incremento stagione: (", prezzo_giornaliero, "+", incremento_stagione,")*", stagioni[s],"=", (prezzo_giornaliero+int(incremento_stagione))*stagioni[s])
                prezzo_totale = prezzo_totale + (prezzo_giornaliero+int(incremento_stagione))*stagioni[s]
        
            print("------ TOTALE: ", prezzo_totale)
            quotes.append(grpc_pb2.quote(beachClub=lido_id, computedPrice=prezzo_totale))
        
        response = grpc_pb2.quoteResponse(quotes = quotes)
        return response



    def insertPrices (self, request, context):
        """ set the prices for the items according the entered value

        Args:
            request (grpc_pb2.priceRequest): grpc message containing the details of the prices
            context (_type_): 

        Returns:
            grpc_pb2.response: grpc message containing the outcome boolean and the description message
        """

        try :
            print("Il server ha ricevuto:")
            print(request.username, request.priceOmbrellone,request.priceSdraio, request.priceLettino, request.priceSedia, 
                request.incrPrimeFile, request.incrAltaStagione, request.incrBassaStagione, request.incrMediaStagione)

            dict = {"ombrellone" : request.priceOmbrellone, "sdraio" : request.priceSdraio, "lettino" : request.priceLettino,"sedia" : request.priceSedia}
            
            expressionAttributeValues = {}
            transactions = []
            for key in dict:
                update = self.db.updateTransaction([['lidoId','S',request.username],['pezzo','S',key]],[['costo','N',dict[key]]],'pricePerPiece')
                transactions.append(update)

           
            update = self.db.updateTransaction([['lidoId','S',request.username],['row','S','1']],[['incr','N',request.incrPrimeFile]],'pricePerRow')
            transactions.append(update)

            
            dict = {"incrAltaStagione" : request.incrAltaStagione,
            "incrBassaStagione" : request.incrBassaStagione,
            "incrMediaStagione" : request.incrMediaStagione} 

            for key in dict:
                update = self.db.updateTransaction([['lidoId','S',request.username],['season','S',key]],[['incr','N',dict[key]]],'pricePerSeason')
                transactions.append(update)
            
            reponse, msg = self.db.executeTransaction (transactions)
            
            if reponse ==  False:
                return grpc_pb2.response(operationResult = False,errorMessage = msg)

        except Exception as e:
            print (repr(e))
            return grpc_pb2.response(operationResult = False,errorMessage = "Insertion has failed")
        response = grpc_pb2.response(operationResult = True,errorMessage = "Insertion has succeded")
        return response




server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_QuoteServicer_to_server(QuotesServicer(), server)
print('Starting QUOTE SERVICE. Listening on port 50053.')
server.add_insecure_port('[::]:50053')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)