from concurrent import futures
from datetime import datetime, timedelta
import threading
import time
import grpc
import pika
import uuid
from geopy.geocoders import Nominatim
import haversine as hs
import numpy as np
import ssl
import certifi
import geopy.geocoders
from decimal import Decimal
from dBUtils import DBUtils
from reservationLogic import ReservationLogic
import boto3
from proto import grpc_pb2
from proto import grpc_pb2_grpc
import os

class ReservationServicer(grpc_pb2_grpc.ReservationServicer):
    
    def __init__(self):

        
        self.db = DBUtils()
        self.logic = ReservationLogic()
        dynamoDb = boto3.resource('dynamodb', region_name='us-east-1')
        self.prenotazione = dynamoDb.Table('prenotazione')              # serve per la manual reservation
        self.storiaUtente = dynamoDb.Table('storiaUtente')


        self.connectionEmail =  None
        self.channelEmail = None
        self.connectionSAGA = None
        self.channelSAGA = None
        self.requestQueue = None
        self.responseQueue = None
        self.corr_id = None
      
        accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
        self.stubAccounting = grpc_pb2_grpc.AccountingStub(accountingChannel)
        
        
    def on_open (self):
        try:
            print ("CONNECTION OPEN")
            self.channelEmail = self.connectionEmail.channel()   
            return self.on_channel_open()

        except Exception as e:
            print(repr(e))
            if self.connectionEmail != None:
                self.connectionEmail.close()
            return False

    
    def on_open_SAGA(self):
        try:
            print ("CONNECTION OPEN FOR SAGA")
            self.channelSAGA = self.connectionSAGA.channel()
            return self.on_channel_open_SAGA()
        except Exception as e:
            print(repr(e))
            if (self.connectionSAGA != None):
                self.connectionSAGA.close()
            return False
    
    def on_channel_open (self):
        try:
            print("CHANNEL OPEN")
            self.channelEmail.exchange_declare(exchange='topic_logs', exchange_type='topic')
            return self.on_exchange()
        except Exception as e:
            print(repr(e))
            if self.connectionEmail != None:
                self.connectionEmail.close()
            return False
    
    
    def on_channel_open_SAGA (self):
        try:
            print("CHANNEL CORRECTLY CREATED")
            
            # Dichiarazione per le code delle richieste e delle risposte
            self.channelSAGA.queue_declare(queue="Pay_request")
            self.channelSAGA.queue_declare(queue="Pay_response") 
        
            self.channelSAGA.queue_declare(queue="History_request")
            self.channelSAGA.queue_declare(queue="History_response")
            
            self.publishRequest = "History_request"
            
            
            # quando consuma da History_request deve eseguire l'update della storia utente
            self.channelSAGA.basic_consume(
                    queue="History_request",
                    on_message_callback=self.updateUserHistory,
                    auto_ack=True)

            # quando consuma da pay_response valuta se eseguire il rollback oppure no
            self.channelSAGA.basic_consume(
                    queue="Pay_response",
                    on_message_callback=self.onResponseSaga,
                    auto_ack=True)

            return True

        except Exception as e:
            print(repr(e))
            if (self.connectionSAGA != None):
                self.connectionSAGA.close()
            return False
        
    def on_exchange (self):
        try:
            print('Have exchange')

            #CODA PER TUTTE LE RICHIESTE
            result = self.channelEmail.queue_declare(queue="emailQueue")
            self.requestQueue = result.method.queue

            #CODA PER LE RISPOSTE
            result = self.channelEmail.queue_declare(queue='responseQueue:Reservation') 
            self.responseQueue = result.method.queue

            #BINDING DELLA CODA delle risposte all'exchange con routing key pari a Reservation
            self.channelEmail.queue_bind(exchange='topic_logs', queue=self.responseQueue, routing_key="Reservation.*")
            return self.on_bind()

        except Exception as e:
            print(repr(e))
            if self.connectionEmail != None:
                self.connectionEmail.close()
            return False

    def on_bind(self):

        try:
            self.channelEmail.basic_consume(
                    queue=self.responseQueue,
                    on_message_callback=self.onResponseEmail,
                    auto_ack=True)

            print("Awaiting email responses")
            return True
        except Exception as e:
            print(repr(e))
            if self.connectionEmail != None:
                self.connectionEmail.close()
            return False
    
        

    def getReservedSeats(self, request, context):
        """ get the reserved seats in the specified date

        Args:
            request (grpc_pb2.reservedSeatsRequest): grpc message containing the beach club username and the date
            context (_type_): 

        Returns:
            grpc_pb2.reservedSeatsResponse: grpc message containing a list of association (seat id -> user id)
        """

        lidoId = request.beachClubId
        date = datetime.fromtimestamp(request.date.seconds).date()
        print("sto calcolando i posti riservati in un lido per una giornata")

        data = self.db.scanDb('prenotazione', ['lidoId'], [lidoId])

        reservations = []    
        if len(data) != 0:
            for i in range (0, len(data)):
                fromDate = datetime.strptime(data[i]['fromDate'], "%d/%m/%Y").date()
                toDate = datetime.strptime(data[i]['toDate'], "%d/%m/%Y").date()
                if (date <= toDate and date >= fromDate):
                    reservation = grpc_pb2.reservation(
                        ombrelloneId=data[i]['ombrelloneId'],
                        userId=data[i]['userId']
                    )
                    reservations.append(reservation)
        print("calcolo dei posti finito, ritorno al microservizio chiamante")
        return grpc_pb2.reservedSeatsResponse(reservation=reservations)


    def getListOfProposal(self, proposalRequest, context):
        """ executes a suggestion algorithm in order to show to the user the proposals closest to his interests and wishes. 
            The price and distance entered can vary according to previous user's reservations

        Args:
            proposalRequest (grpc_pb2.proposalRequest): grpc message containing the filters for the suggestion (location, 
            numRow, numBeachUmbrella, numLettini, numSdraio, numChair, fromDate, toDate, maxPrice, sessione)
            context (_type_): 

        Returns:
            grpc_pb2.proposalResponse: grpc message containing a list of associations (lido_id,city,distance,price,averageReview,index)
        """

        print("Il server ha ricevuto:")
        print(proposalRequest.location, proposalRequest.numRow, proposalRequest.numBeachUmbrella, proposalRequest.numLettini, proposalRequest.numSdraio, proposalRequest.numChair, proposalRequest.maxPrice, proposalRequest.sessione.dict[0].value)
        
        maxDistance = 20                                    # raggio entro cui si cercano le offerte
        budget = proposalRequest.maxPrice                   # prezzo massimo per un'offerta
        location = proposalRequest.location + " Italy"      # centro del cerchio di ricerca
        allowCorrelation = False                            # suggerimenti basati su correlazione disabilitati per default
        

        # 0. prendo le informazioni della storia utente
        try:
            username = proposalRequest.sessione.dict[0].value
            data = self.db.scanDb('storiaUtente', ['userId'], [username])
            print("user history: ".format(data))
            
            if len(data) != 0:
                mediaDistanza = float(data[0]['mediaDistanza'])
                varianzaDistanza = float(data[0]['varianzaDistanza'])
                mediaDifferenzaBudget = float(data[0]['mediaDifferenzaBudget'])
                varianzaDifferenzaBudget = float(data[0]['varianzaDifferenzaBudget'])
                counter = int(data[0]['tot'])
                nRistorazione = data[0]['nRistorazione']
                nBar = data[0]['nBar']
                nCampi = data[0]['nCampi']
                nAnimazione = data[0]['nAnimazione']
                nPalestra = data[0]['nPalestra']

                if counter >= 3:                                # la storia utente influenza la recommendation a partire dalla 4a prenotazione
                    allowCorrelation = True
                    
                    newBudget = budget-mediaDifferenzaBudget+varianzaDifferenzaBudget/counter
                    if newBudget>0:
                        budget = min(budget, newBudget)
                    maxDistance = min(maxDistance, mediaDistanza+varianzaDistanza/counter)
                    reference = [float(nRistorazione)/counter, float(nBar)/counter, float(nCampi)/counter, float(nAnimazione)/counter, float(nPalestra)/counter]
                    print('new budget: {}; new search distance: {}'.format(budget, maxDistance))


            # 1. calcolo i preventivi di tutti i lidi

            quoteChannel = grpc.insecure_channel("{}:50053".format("quote"))
            stubQuote = grpc_pb2_grpc.QuoteStub(quoteChannel)
            response = stubQuote.computeQuotes(grpc_pb2.quoteForm(
                numRow=proposalRequest.numRow, 
                numUmbrella=proposalRequest.numBeachUmbrella,
                numLettini=proposalRequest.numLettini,
                numSdraio=proposalRequest.numSdraio,
                numChair=proposalRequest.numChair,
                fromDate=proposalRequest.fromDate,
                toDate=proposalRequest.toDate,
                sessione=proposalRequest.sessione
            ))

            print("PREVENTIVI PER OGNI LIDO:")
            print(response)

            # 2. elimino i lidi che sforano il budget
            offerte_compatibili = {}
            for preventivo in response.quotes:
                costo = preventivo.computedPrice
                if costo <= budget:
                    lido_id = preventivo.beachClub
                    offerte_compatibili[lido_id] = costo

            print("OFFERTE COMPATIBILI:")
            print (offerte_compatibili)

            reviewChannel = grpc.insecure_channel("{}:50054".format("review"))
            stubReview = grpc_pb2_grpc.ReviewStub(reviewChannel)

            # 3. calcola le coordinate della locazione richiesta dall'utente
            try:
                ctx = ssl.create_default_context(cafile=certifi.where())
                geopy.geocoders.options.default_ssl_context = ctx
                loc = Nominatim(user_agent="GetLoc",timeout=3)
                getLocRequest = loc.geocode(location)
                lat = getLocRequest.latitude
                lon = getLocRequest.longitude
                locRequest = (lat, lon)
                
            except Exception as e:
                print(repr(e))
                return grpc_pb2.proposalResponse(offerta= [])

            print("[address requested] : {}\n\tlatitude: {}\n\tlongitude: {}".format(getLocRequest.address, lat, lon))
            
            listLevel1 = []
            listLevel2 = []
            listLevel3 = []  
        
            for lido_id in offerte_compatibili:

                    try:
                        # 4. calcola la distanza di ogni lido dalla città selezionata dall'utente ed elimina quelli più lontani
                        lido = self.stubAccounting.getBeachClubDetails(grpc_pb2.reviewRequest(usernameBeachClub=lido_id))   
                        city = lido.location + " Italy"

                        getLocLido = loc.geocode(city)
                        locLido = (getLocLido.latitude, getLocLido.longitude)
                        distance = hs.haversine(locRequest, locLido)
                        print("[address ", lido_id, "] :", getLocLido.address, " --> distanza (km): ", distance)

                    except Exception as e:
                        print(repr(e))
                        return grpc_pb2.proposalResponse(offerta=[])

                    if distance>maxDistance:
                        print("     (!) lido troppo distante, eliminato")
                
                    else:  

                            # 5. calcolo il voto medio dei lidi nel raggio di 10 km e calcola la correlazione
                            response = stubReview.getAverageScoreOfBeachClub(grpc_pb2.reviewRequest(usernameBeachClub=lido_id))

                            dettagli_lido = []
                            dettagli_lido.append(lido_id)
                            dettagli_lido.append(getLocLido.address)
                            dettagli_lido.append(distance)
                            dettagli_lido.append(offerte_compatibili[lido_id])
                            dettagli_lido.append(response.average)

                            # 6. il lido va in una tra 3 liste in base alla sua correlazione con la storia utente (ALTA, MEDIA, BASSA)

                            if allowCorrelation == True:

                                # trovo la correlazione tra le facilities cercate in media 
                                # dal cliente e l'offerta del lido attualmente considerato

                                ristorazione = 1 if lido.ristorazione==True else 0
                                bar = 1 if  lido.bar==True else 0
                                campi = 1 if  lido.campi==True else 0
                                animazione = 1 if  lido.animazione==True else 0
                                palestra = 1 if  lido.palestra==True else 0
                                activity = [ristorazione, bar, campi, animazione, palestra]
                                correlation = np.corrcoef(reference, activity)[0,1]

                                if correlation > 0.5:
                                    listLevel1.append(dettagli_lido)
                                elif correlation>0:
                                    listLevel2.append(dettagli_lido)
                                else:
                                    listLevel3.append(dettagli_lido)  
                                    
                            else:
                                print("OK")
                                listLevel1.append(dettagli_lido)

            

            # 7. ordino le 3 liste in base alle recensioni e ritorno le offerte mostrando prima i gruppi con più correlazione
            sortedProposals = []
            sortedProposals.append(sorted(listLevel1, key=lambda k: k[4], reverse=True))
            sortedProposals.append(sorted(listLevel2, key=lambda k: k[4], reverse=True))
            sortedProposals.append(sorted(listLevel3, key=lambda k: k[4], reverse=True))
            print("sorted proposal=", sortedProposals)
            print("LISTA DEFINITIVA\n\t*offerte adatte a te: {}\n\t*offerte poco adatte: {}\n\t*offerte lontane dai tuoi gusti: {}".format(sortedProposals[0], sortedProposals[1], sortedProposals[2]))
            
            base = 0
            list = []
            for sList in sortedProposals:
                lenght = len(sList)
                for i in range (0, lenght):
                    proposalResponse = grpc_pb2.proposal(
                        lido_id = sList[i][0],
                        city = sList[i][1],
                        distance = sList[i][2],
                        price = sList[i][3],
                        averageReview = sList[i][4],
                        index = i + base
                    )
                    list.append(proposalResponse)
                base = base + lenght
        except grpc._channel._InactiveRpcError as e:
             print("Microservice quote is not currently running")
             return grpc_pb2.proposalResponse(offerta=None) 
        except Exception as e:
            print(repr(e))
            return grpc_pb2.proposalResponse(offerta=None)    
        return grpc_pb2.proposalResponse(offerta=list)
        
    

    def reserve(self, reservationRequest, context):
        """ perform the reservation checking that all constraints are respected. If requested, trigger the online payment (SAGA).

        Args:
            reservationRequest (grpc_pb2.reservationRequest): grpc message containing the new reservation's details
            context (_type_): 

        Returns:
            grpc_pb2.response: grpc message containing the outcome boolean and the description message
        """

        try:
            username = reservationRequest.sessione.dict[0].value
            email    = reservationRequest.sessione.dict[2].value    
            lido_id  = reservationRequest.beachClubId

            fromDate    = datetime.fromtimestamp(reservationRequest.fromDate.seconds).date()
            toDate      = datetime.fromtimestamp(reservationRequest.toDate.seconds).date()
            costo       = reservationRequest.price
            payOnline   = reservationRequest.payOnline

            nFila           = int(reservationRequest.numRow)
            nUmbrella       = int(reservationRequest.numUmbrella)
            nLettini        = int(reservationRequest.numLettini)
            nSdraio         = int(reservationRequest.numSdraio) 
            nChair          = int(reservationRequest.numChair)
            distance        = reservationRequest.distance
            budgetDifference= reservationRequest.budgetDifference
            idCard          = int(reservationRequest.idCard)
            
            print("Username:{}, lido:{}, fila:{}, num Ombrelloni: {}, numero lettini: {}, numero sdraio: {}, numero sedie: {}, from: {}, to: {}, prezzo concordato: {}, Pagamento online: {}, distanza: {}, differenza col budget: {}".format (
                username, lido_id,nFila ,nUmbrella,nLettini,nSdraio,nChair, fromDate, toDate, costo, payOnline, distance,budgetDifference))
            
            # 1. controlla che le postazioni, sdraio, lettini e sedie siano disponibili 
            
            totOmbrelloniPerFila,err1 = self.logic.totaleOmbrelloniPerFila(lido_id,nFila)
            if totOmbrelloniPerFila == None:
                print(err1)
                return  grpc_pb2.response(operationResult = False, errorMessage = err1)
            print("TOTALE OMBRELLONI PER FILA: {}".format(totOmbrelloniPerFila))
            totPezzi, err2 = self.logic.totPezzi(lido_id)
            if totPezzi == None:
                print(err2)
                return  grpc_pb2.response(operationResult = False, errorMessage = err2)
            print("TOTALE PEZZI: {}".format(totPezzi))
            
            date_generated = [fromDate + timedelta(days=x) for x in range(0, (toDate-fromDate).days + 1)]
            
            dict = {}
            for date in date_generated:
                
                reservationsPerDate,ombrelloniOccupatiPerDateAndRow,pezziOccupati,err3 = self.logic.getReservations (lido_id, date, nFila) 
                print(reservationsPerDate)
                print(ombrelloniOccupatiPerDateAndRow)
                print(pezziOccupati)
                if reservationsPerDate == None or ombrelloniOccupatiPerDateAndRow == None or pezziOccupati == None:
                    print(err3)
                    return  grpc_pb2.response(operationResult = False, errorMessage = err3)
                strDate = date.strftime("%d/%m/%Y")
                if (totPezzi['totaleSdraio'] - pezziOccupati['sdraioOccupate'] - nSdraio < 0):
                     return  grpc_pb2.response(operationResult = False, errorMessage = "sdraio non dispnibili per {}".format(strDate))
                if (totPezzi['totaleLettini'] - pezziOccupati['lettiniOccupati'] -nLettini < 0):
                     return  grpc_pb2.response(operationResult = False, errorMessage = "lettini non dispnibili per {}".format(strDate))
                if (totPezzi['totaleSedie'] - pezziOccupati['sedieOccupate'] - nChair < 0):
                     return  grpc_pb2.response(operationResult = False, errorMessage = "sdraio non dispnibili per {}".format(strDate))
                if(totOmbrelloniPerFila - len(reservationsPerDate) - nUmbrella) < 0:
                     return  grpc_pb2.response(operationResult = False, errorMessage = "seats not available on {}".format(strDate))

                ombrelloniMancanti = [ele for ele in range (1,totOmbrelloniPerFila + 1 ) if ele not in ombrelloniOccupatiPerDateAndRow]
                dict[strDate] = ombrelloniMancanti

            print("LISTA OMBRELLONI MANCANTI: {}".format(dict))
            # Ho un dizionario del tipo: {30/09/2022: [1,5,7] <-- Ombrelloni non occupati in quella data in quella fila}
            # Come scegliere gli ombrelloni ???
            first = True
            posti_liberi = []
            for key in dict:
                if first==True:
                   posti_liberi = set(dict[key])
                   first = False
                   continue
                posti_liberi = posti_liberi.intersection(dict[key])
                
            if len(posti_liberi) < nUmbrella:
                print("Non sono stati trovati posti validi per tutto il periodo, provo con altre soluzioni ...")
                 
                transactions = []

                for key in dict:
                    #se ci sono posti allora popola il database altrimenti dai un messaggio di errore

                    if len(dict[key]) < nUmbrella:
                        return grpc_pb2.response(operationResult = False, errorMessage = "Seats are not enough on {}".format(key)) 

                    for i in range (0, nUmbrella):

                        sdraioToInsert = nSdraio // nUmbrella
                        lettiniToInsert = nLettini // nUmbrella
                        chairToInsert = nChair // nUmbrella

                        if i == 0:
                            sdraioToInsert +=  nSdraio % nUmbrella
                            lettiniToInsert += nLettini % nUmbrella
                            chairToInsert += nChair % nUmbrella
                    
                        id = uuid.uuid1()

                        put = [['prenotazioneId','N', id.time], ['lidoId','S',lido_id],
                        ['userId','S',username],['fromDate','S',key],['toDate','S',key],
                        ['ombrelloneId','S',"{}x{}".format(nFila,dict[key][i])],['nSdraio','N',sdraioToInsert],
                        ['nLettini','N', lettiniToInsert],['nSedie','N', chairToInsert],['costo','N',costo]]

                        transactions.append(self.db.putTransaction(put,'prenotazione'))
                    response = self.db.executeTransaction(transactions)

                    if response == None:
                        msg = "Transaction has been aborted"
                        return grpc_pb2.response(operationResult = False, errorMessage = msg) 


            else:
                print("Esiste almento un posto valido per tutto il periodo")
                transactions = []  
                for i in range (0,nUmbrella):

                    sdraioToInsert = nSdraio // nUmbrella
                    lettiniToInsert = nLettini // nUmbrella
                    chairToInsert = nChair // nUmbrella

                    if i == 0:
                        sdraioToInsert +=  nSdraio % nUmbrella
                        lettiniToInsert += nLettini % nUmbrella
                        chairToInsert += nChair % nUmbrella

                    id = uuid.uuid1()

                    put = [['prenotazioneId','N', id.time], ['lidoId','S',lido_id],
                        ['userId','S',username],['fromDate','S', fromDate.strftime("%d/%m/%Y")],['toDate','S', toDate.strftime("%d/%m/%Y")],
                        ['ombrelloneId','S',"{}x{}".format(nFila,posti_liberi.pop())],['nSdraio','N',sdraioToInsert],
                        ['nLettini','N', lettiniToInsert],['nSedie','N', chairToInsert],['costo','N',costo]]

                    transactions.append(self.db.putTransaction(put,'prenotazione'))
                    response = self.db.executeTransaction(transactions)
                     
                    if response == None:
                        msg = "Transaction has been aborted"
                        return grpc_pb2.response(operationResult = False, errorMessage = msg) 

          
            # 3. se il pagamento è online inizia SAGA 
            if (payOnline == True):
    
                result,errorMsg = self.establishConnectionSAGA ()

                if result == False:
                   return  grpc_pb2.response(operationResult = False,
                    errorMessage =errorMsg) 
                
                # 4. pubblica un messaggio  per triggerare il pagamento
                request = "{}:{}:{}:{}:{}:{}:{}:{}".format (id.time,username, email, lido_id, costo, distance, budgetDifference, idCard)
                print("SENDING A PAYMENT REQUEST TO {} WITH EMAIL {}".format(username, email))
                
                self.publish(request, 'Pay_request')  
                # self.connectionSAGA.process_data_events(time_limit=None)     
                self.channelSAGA.start_consuming()   #eli
                print("END SAGA")

        except Exception as e:

            msg = "Error in the reservation phase"
          
            print(repr(e))
            return grpc_pb2.response(operationResult = False, errorMessage = msg) 
        
        return grpc_pb2.response(operationResult = True, errorMessage = "La prenotazione ha avuto successo")


    def manualReserve(self, request, context):
        """ perform the reservation triggered by beach club on a specific seat. These seats are not associated with a 
        user and the beach club must insert the customer's name.

        Args:
            request (grpc_pb2.manualReservationRequest): grpc message with the details of the reservation to insert
            context (_type_): 

        Returns:
            grpc_pb2.response: grpc message containing the outcome boolean and the description message
        """
        try:
            username = request.customer
            lido_id =request.beachClubId
            date = datetime.now().date()
            ids = request.ombrelloneId
            nLettini = request.numLettini
            nSdraio= request.numSdraio 
            nChair = request.numChair

            print("Username:{}, lido:{}, da riservare:{}, numero lettini: {}, numero sdraio: {}, numero sedie: {}, from: {}, to: {}".format (
                    username, lido_id, ids, nLettini,nSdraio,nChair, date, date))

            # 1. Cerco tutte le prenotazioni per un lido
            data = self.db.scanDb('prenotazione', ['lidoId'], [lido_id])
            if data == None:
                msg = "OPS ... Errore nella richiesta al database"
                print(msg)
                return  grpc_pb2.response(operationResult = False, errorMessage = msg)
                 
            pezziOccupati = {'sdraioOccupate':0,'lettiniOccupati' :0,'sedieOccupate':0}
            
            for i in range(0, len(data)):                  
                
                # 2. Incremento il numero di sdraio occupate se la prenotazione su cui sto iterando comprende la data odierna
                fromDate = datetime.strptime(data[i]['fromDate'], "%d/%m/%Y").date()  
                toDate = datetime.strptime(data[i]['toDate'], "%d/%m/%Y").date()
                if (date <= toDate and date >= fromDate):
                    # response.append(data[i]['prenotazioneId'])
                    # ombrelloniOccupati.append(int(data[i]['ombrelloneId'][2:]))
                    pezziOccupati['sdraioOccupate'] = pezziOccupati['sdraioOccupate'] + int(data[i]['nSdraio'])
                    pezziOccupati['lettiniOccupati'] = pezziOccupati['lettiniOccupati'] + int(data[i]['nLettini'])
                    pezziOccupati['sedieOccupate'] = pezziOccupati['sedieOccupate'] +  int(data[i]['nSedie'])
                
                    # 3. Se incontro una prenotazione per il posto che sto cercando di riservare ritorno un errore
                    if data[i]['ombrelloneId'] in ids:
                        msg = "OPS ... Una tra le postazioni inserite è occupata, riaggiorna la pagina"
                        print(msg)
                        return  grpc_pb2.response(operationResult = False, errorMessage = msg)
            
            # 3. controlla la disponibilità dei pezzi
            totPezzi, err2 = self.logic.totPezzi(lido_id)
            if totPezzi == None:
                print(err2)
                return  grpc_pb2.response(operationResult = False, errorMessage = err2)
            
        
            strDate = date.strftime("%d/%m/%Y")
            if (totPezzi['totaleSdraio'] - pezziOccupati['sdraioOccupate'] -nSdraio < 0):
                return  grpc_pb2.response(operationResult = False, errorMessage = "sdraio non dispnibili per {}".format(strDate))
            if (totPezzi['totaleLettini'] - pezziOccupati['lettiniOccupati'] -nLettini < 0):
                return  grpc_pb2.response(operationResult = False, errorMessage = "lettini non dispnibili per {}".format(strDate))
            if (totPezzi['totaleSedie'] - pezziOccupati['sedieOccupate'] - nChair < 0):
                return  grpc_pb2.response(operationResult = False, errorMessage = "sdraio non dispnibili per {}".format(strDate))
            
            for id in ids:
                keyid = uuid.uuid1()
                self.prenotazione.put_item(
                    Item= {
                        'prenotazioneId': int(keyid.time),
                        'lidoId': lido_id,
                        'userId': username,
                        'fromDate': date.strftime("%d/%m/%Y"),
                        'toDate': date.strftime("%d/%m/%Y"),
                        'ombrelloneId': id,
                        'nSdraio': int(nSdraio),
                        'nLettini': int(nLettini),
                        'nSedie': int(nChair),
                        'costo': 0
                    }
                )
                # 4. se prenoto più postazioni insieme il conto dei pezzi lo metto solo in una entry del db
                nSdraio = 0
                nLettini = 0
                nChair = 0

        except Exception as e:
            print(repr(e))
            # return grpc_pb2.response(operationResult = False, errorMessage = "Exception has occurred in manual reservation")
            return grpc_pb2.response(operationResult = False, errorMessage = repr(e))

        return grpc_pb2.response(operationResult = True, errorMessage = "Manual reservation has succeded") 
        
    
             
    def establishConnectionEmail (self):
        """ Create a new instance of the Connection Object for RabbitMQ, then create a new channel and declares request and response queues
            for sending the email

        Returns:
            BOOL: return TRUE if the connection to RabbitMQ server has succeded
        """
        try :
            amqp_url = os.environ['AMQP_URL']

            parameters = pika.URLParameters(amqp_url)
            self.connectionEmail = pika.BlockingConnection(parameters)
            
            return self.on_open(),"Connection and queues are correctly established"
        
        except KeyboardInterrupt:
            if (self.connectionEmail != None):
                self.connectionEmail.close()
       
        except Exception as e:
            print(repr(e))
        return False,"Error in establishing connections and queues"

    def establishConnectionSAGA (self):
        """  Create a new instance of the Connection Object for RabbitMQ, then create a new channel and declares request and response queues
             for implementing Saga pattern

        Returns:
            BOOL,String: Return a Boolean in order to discriminate the success or failure of the method and an error message
        """

        try :
            amqp_url = os.environ['AMQP_URL']
            parameters = pika.URLParameters(amqp_url)
            self.connectionSAGA = pika.BlockingConnection(parameters)

            return self.on_open_SAGA(),"Connection and queues are correctly established"
        except KeyboardInterrupt:
            if (self.connectionSAGA != None):
                self.connectionSAGA.close()
        except Exception as e:
            print(repr(e))

            if (self.connectionSAGA != None):
                self.connectionSAGA.close()

        return False,"Error in establishing connection"


        
        
    def updateUserHistory(self, ch, method, properties, body):
        
        print("\nUPDATE USER HISTORY phase has started: from History_request to History_response")
        try:
            request = body.decode("utf-8").split(':')
            id = request[0]
            username = request[1]
            email = request[2]
            lido_id = request[3]
            costo = int(request[4])
            distance = float(request[5])
            budgetDifference=float(request[6])
            cardId = int(request[7])

            print("[Storia utente] Username:{}, distanza:{}, differenza dal budget: {}".format (
                    username, distance, budgetDifference))

            
            # 1. Leggi i valori della tabella per l'utente, se esistono
            data = self.db.scanDb('storiaUtente', ['userId'], [username])
            
            # 2. se non esistono valori inizializzo tutto a 0
            if len(data) == 0:
                mediaDistanza = mediaDifferenzaBudget = 0.0
                varianzaDistanza = varianzaDifferenzaBudget = 0.
                counter = 0
                nRistorazione = nBar = nCampi = nAnimazione = nPalestra = 0
            else:
                mediaDistanza = float(data[0]['mediaDistanza'])
                varianzaDistanza = float(data[0]['varianzaDistanza'])
                mediaDifferenzaBudget = float(data[0]['mediaDifferenzaBudget'])
                varianzaDifferenzaBudget = float(data[0]['varianzaDifferenzaBudget'])
                counter = int(data[0]['tot'])
                nRistorazione = data[0]['nRistorazione']
                nBar = data[0]['nBar']
                nCampi = data[0]['nCampi']
                nAnimazione = data[0]['nAnimazione']
                nPalestra = data[0]['nPalestra']
            
            # 3. incrementa il contatore delle caratteristiche che l'utente ha scelto nei lidi

            responseAccounting = self.stubAccounting.getBeachClubDetails(grpc_pb2.reviewRequest(usernameBeachClub=lido_id))
            if responseAccounting.ristorazione == True:
                nRistorazione = nRistorazione + 1
            if responseAccounting.bar == True:
                nBar = nBar +1
            if responseAccounting.campi == True:
                nCampi = nCampi +1
            if responseAccounting.animazione == True:
                nAnimazione = nAnimazione + 1
            if responseAccounting.palestra == True:   
                nPalestra = nPalestra + 1
            
            # 4. aggiorna le medie e le varianze
            varianzaDistanza = varianzaDistanza + (counter/(counter+1))*((distance-mediaDistanza)**2)
            varianzaDifferenzaBudget = varianzaDifferenzaBudget + (counter/(counter+1))*((budgetDifference-mediaDifferenzaBudget)**2)

            mediaDistanza = mediaDistanza + (distance-mediaDistanza)/(counter+1)
            mediaDifferenzaBudget = mediaDifferenzaBudget + (budgetDifference-mediaDifferenzaBudget)/(counter+1)
            
            counter = counter + 1
            

            # 5. aggiorna le entry nel database per le recommendation
            expressionAttributeValues = {":val1": Decimal (int(mediaDistanza)),":val2": Decimal(int(varianzaDistanza)),":val3": Decimal(int(mediaDifferenzaBudget)),
            ":val4": Decimal(int(varianzaDifferenzaBudget)),":val5": counter, ":val6": nRistorazione,":val7": nBar,":val8": nCampi,
            ":val9": nAnimazione,":val10": nPalestra }
        
            self.storiaUtente.update_item (
                Key = {
                             'userId': username,
                        },
                UpdateExpression= "SET mediaDistanza= :val1, varianzaDistanza =:val2, mediaDifferenzaBudget =:val3, varianzaDifferenzaBudget =:val4, tot =:val5, nRistorazione =:val6, nBar =:val7, nCampi =:val8, nAnimazione =:val9, nPalestra =:val10",
                ExpressionAttributeValues=expressionAttributeValues,
                ReturnValues = "ALL_NEW",
            )
            
            msg = "Saga completed correctly"
            print("[Update user history]:", msg)
            request = "SUCCESS:{}:{}:{}:{}:{}:{}:{}".format(id,username,email,lido_id,costo,cardId,msg)
            
            self.publish(request, 'History_response')

        except Exception as e:
            print(repr(e))
            errorMsg = "Update user history operation has failed"
            request = "FAILURE:{}:{}:{}:{}:{}:{}:{}".format(id,username,email,lido_id,costo,cardId,errorMsg)
            self.publish(request, 'History_response')


    def onResponseEmail (self, ch, method, properties, body):
        print("RESPONSE: %r:%r" % (method.routing_key, body))
        if self.connectionEmail != None and self.connectionEmail.is_open:
            self.connectionEmail.close()
    
    def onResponseSaga (self, ch, method, properties, body):
        try:
            #RESPONSE-> SUCCESS:Prenotazione_ID:username:Email:msg 
            response = body.decode("utf-8").split(':')
            print("\nRESPONSE Saga from Pay_response: {}".format(response))
            esito = str(response[0])
            prenotazione_id = int(response[1])
            username = response[2]
            email = response[3]
            msg = response[4] 
            
            self.responseMsg = msg
            if (esito != "SUCCESS"):

                # 1. fare il rollback dell'inserimento della prenotazione
                print("ROLLBACK operation: Deleting reservation previously inserted")
                data = self.db.scanDb('prenotazione', ['prenotazioneId'], [prenotazione_id])
                print("1")
                for i in range (0,len(data)) :
                    result1 = self.prenotazione.delete_item (
                        Key ={
                            'prenotazioneId' : prenotazione_id,
                            'ombrelloneId' : str(data[i]['ombrelloneId'])
                            },
                        ReturnValues = 'ALL_OLD'
                    )
                    print("[cancellazione prenotazione] result=", result1)  
            
            
            else:   
                result, errorMsg = self.sendEmail (username, email)
                print ("result:{}, ErrorMsg:{}".format(result, errorMsg))
            
        
        except Exception as e:
            print(repr(e))
            
        finally:
            if self.channelSAGA != None:
                self.channelSAGA.stop_consuming()

            if self.connectionSAGA != None and self.connectionSAGA.is_open:
                    self.connectionSAGA.close()  
            

    def publish(self, request, routingKey):
        print (request, routingKey)        
        self.corr_id = str(uuid.uuid4())
        self.channelSAGA.basic_publish(
            exchange='',
            routing_key=routingKey,
            properties=pika.BasicProperties(
                correlation_id=self.corr_id,
            ),
            body=request)



    def sendEmail(self, username, email):
        try :
            result = self.establishConnectionEmail ()
            if result == False:
                return False

            request = "{}:{}#Reservation".format (username,email)
            #INVIO DEL MESSAGGIO DI RICHIESTA
            print("SENDING AN EMAIL TO {}".format(request))
            self.corr_id = str(uuid.uuid4())
            self.channelEmail.basic_publish(
                exchange='',
                routing_key='emailQueue',
                properties=pika.BasicProperties(
                    correlation_id=self.corr_id,
                ),
                body=request)
        
            self.connectionEmail.process_data_events(time_limit=None)
        except Exception as e:
            print(repr(e))
           
            return False , "Send operation has failed"
        return True, "Send operation has succeded"


service = ReservationServicer()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_ReservationServicer_to_server(service, server)
print('Starting RESERVATION SERVICE. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

# def grpc_server (service):
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     grpc_pb2_grpc.add_ReservationServicer_to_server(service, server)
#     print('Starting RESERVATION SERVICE. Listening on port 50051.')
#     server.add_insecure_port('[::]:50051')
#     server.start()

#     try:
#         while True:
#             time.sleep(86400)
#     except KeyboardInterrupt:
#         server.stop(0)

# def sagaQueueConsumer(service):
#     print(" [x] Awaiting SAGA reservation requests")
#     service.channelSAGA.start_consuming()
    
# service = ReservationServicer()
# x = threading.Thread(target=grpc_server, args=(service,))
# x.start()

# y = threading.Thread(target=sagaQueueConsumer, args=(service,))
# y.start()
# x.join()