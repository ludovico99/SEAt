import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from geopy.geocoders import Nominatim
import haversine as hs
import geopy.geocoders
import ssl
import certifi
import datetime


class ReservationGateway():

    def __init__(self):
      self.reservationChannel = grpc.insecure_channel("{}:50051".format("localhost"))
      self.stubReservation = grpc_pb2_grpc.ReservationStub(self.reservationChannel)

    def getSuggestions (self,details):

        numRow = int(details['num_fila'])
        numUmbrella = int(details['num_ombrelloni'])
        numLettini = int(details['num_lettini'])
        numSdraio = int(details['num_sdraio'])
        numChair = int(details['num_sedie'])
            
        fromDate = details['fromDate']
        toDate = details['toDate']

        timestamp1 = Timestamp()
        timestamp1.FromDatetime(fromDate)   
        timestamp2 = Timestamp()
        timestamp2.FromDatetime(toDate) 
        
        prezzoMassimo = int (details['price'] )
        city = details['city']

        list = []
        list.append(grpc_pb2.dictionary(key = "username", value=details['username']))
        list.append(grpc_pb2.dictionary(key = "tipoUtente", value=details['type']))
        list.append(grpc_pb2.dictionary(key = "email", value = details['email'] ))
        sessione = grpc_pb2.session(dict = list)

        response = self.stubReservation.getListOfProposal(grpc_pb2.proposalRequest(
            location=city,
            numRow=numRow,
            numBeachUmbrella=numUmbrella,
            numLettini=numLettini,
            numSdraio=numSdraio,
            numChair=numChair,
            fromDate=timestamp1,
            toDate=timestamp2,
            maxPrice=prezzoMassimo,
            sessione=sessione
        ))

        suggestions = []
        for offerta in response.offerta:
            proposta = [offerta.lido_id, offerta.city, round(int(offerta.distance), 2), offerta.price, round(int(offerta.averageReview),2), offerta.index]
            suggestions.insert(offerta.index, proposta)
        
        return suggestions


    def getReservedSeatMatrix(self,lido_id, configurationMatrix):
        matrix = []

        date = datetime.datetime.now()
        timestamp = Timestamp()
        timestamp.FromDatetime(date)

        response = self.stubReservation.getReservedSeats(grpc_pb2.reservedSeatsRequest(
            beachClubId = lido_id,
            date=timestamp
        ))

        matrix =[]
        for lenFila_i in configurationMatrix:
            # configurationMatrix =  (numfila1, num fila2, ...)
            reservationRow_i = []
            for k in range(0, lenFila_i):
                reservationRow_i.append("")
            matrix.append(reservationRow_i)
        
        for prenotazione in response.reservation:
            row = int(prenotazione.ombrelloneId[0]) - 1
            col = int(prenotazione.ombrelloneId[2:]) - 1
            matrix[row][col] = prenotazione.userId
                
        return matrix

    def reserve (self, form_detail, selected_proposal, idCard):

        beachClubId = selected_proposal[0]
        numRow = form_detail['num_fila']
        numUmbrella = form_detail['num_ombrelloni']
        numLettini = form_detail['num_lettini']
        numSdraio = form_detail['num_sdraio']
        numChair = form_detail['num_sedie']
        fromDate = form_detail['fromDate']
        toDate = form_detail['toDate']

        timestamp1 = Timestamp()
        timestamp1.FromDatetime(fromDate)

        timestamp2 = Timestamp()
        timestamp2.FromDatetime(toDate)

        list = []
        list.append(grpc_pb2.dictionary(key = "username", value=form_detail['username']))
        list.append(grpc_pb2.dictionary(key = "tipoUtente", value=form_detail['type']))
        list.append(grpc_pb2.dictionary(key = "email", value = form_detail['email'] ))
        sessione = grpc_pb2.session(dict = list)

        price = selected_proposal[3]
        payOnline = form_detail['payOnline']

        request_city = form_detail['city']
        selected_city = selected_proposal[1]

        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx

        loc = Nominatim(user_agent="GetLoc",timeout=3)
        getLocRequest = loc.geocode(request_city)
        getLocLido = loc.geocode(selected_city)
        locRequest = (getLocRequest.latitude, getLocRequest.longitude)
        locLido = (getLocLido.latitude, getLocLido.longitude)
        distance = hs.haversine(locRequest, locLido)


        budgetDifference= float(form_detail['price']) - float(selected_proposal[3])
        
        response = self.stubReservation.reserve( grpc_pb2.reservationRequest(
                beachClubId = beachClubId,
                numRow=int(numRow),
                numUmbrella=int(numUmbrella),
                numLettini=int(numLettini),
                numSdraio=int(numSdraio),
                numChair=int(numChair),
                fromDate = timestamp1,
                toDate = timestamp2,
                price = int(price),
                payOnline = payOnline,
                sessione=sessione,
                distance=float(distance),
                budgetDifference=float(budgetDifference),
                idCard=int(idCard)
        ))
        return response.operationResult, response.errorMessage

    def manualReservation(self,lidoId, customerName, numArray):
    
        ombrelloniId=[]
        for id in numArray[0]:
            new_id = "{}x{}".format(id[0],id[1])
            ombrelloniId.append(new_id)

        response = self.stubReservation.manualReserve(grpc_pb2.manualReservationRequest(
                beachClubId = lidoId,
                customer = customerName,
                ombrelloneId  = ombrelloniId,
                numLettini = numArray[1],
                numSdraio = numArray[2],
                numChair = numArray[3] 
        ))
        return response.operationResult, response.errorMessage