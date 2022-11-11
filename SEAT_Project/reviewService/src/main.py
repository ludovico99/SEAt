from concurrent import futures
import time
import grpc
import boto3
from datetime import datetime

from proto import grpc_pb2
from proto import grpc_pb2_grpc
from dBUtils import DBUtils
import socket

class ReviewServicer(grpc_pb2_grpc.ReviewServicer):
    
    def __init__(self):
        self.db = DBUtils()
        self.port = "50054"
        result = self.notifyServiceRegistry(self.port)
        if result == False:
            print("The notification to the service registry has failed. The Accounting service should be unavailable")

    def notifyServiceRegistry (self,port):
        """Send a notification about its port number

        Args:
            port (string): port number of the accounting service

        Returns:
            BOOL: Return True if the message has been sent correctly
        """
        
        try:
            queue_name = "service_registry_queue"
            sqs = boto3.client('sqs',region_name='us-east-1')
            hostname = socket.gethostname()
            ipAddr = socket.gethostbyname(hostname)
            response = sqs.send_message(
            QueueUrl= queue_name,
            DelaySeconds=10,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'Accounting service notification'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'Accounting service'
                },
                
            },
            MessageBody=(
                "My port number is :{}, my ipAddress is :{}, service name :{}, hostname :{}.".format(port, ipAddr, self.__class__.__name__, hostname)
            )
        )

            print(response['MessageId'])
            return True

        except Exception as e:
            print(repr(e))
            return False
        

    def review(self, reviewDetails, context):
        """ Insert a review in the DynamoDB database
        Args:
            reviewDetails (grpc_pb2.reviewDetails): grpc message containing the details of the rewview
            context (_type_): 

        Returns:
            grpc_pb2.response: grpc message containing the outcome boolean and the description message
        """

        print("Il server ha ricevuto:")
        print(reviewDetails.usernameBeachClub, reviewDetails.star, reviewDetails.reviewDetail, reviewDetails.comment)
        msg = ""

        # gli utenti possono assegnare da 1 a 5 stelle
        if reviewDetails.star<1 and reviewDetails.star>5:
            result = False
            msg = "Puoi inserire da 1 a 5 stelle"
        else:
            result = self.db.insertInDb('recensioni', reviewDetails)  

        if result == True:
            msg = "Recensione inserita con successo"
        else:
            msg = "Fallimento nell'inserimento della recensione"
        
        response = grpc_pb2.response(operationResult = result, errorMessage = msg)
        return response



    def getAllReviewsOfBeachClub(self, reviewRequest, context):
        """ Get the list of the reviews for the requested beach club
    
        Args:
            reviewRequest (grpc_pb2.reviewRequest): grpc message containing the beach club username to look for
            context (_type_): 

        Returns:
            grpc_pb2.reviewResponse: grpc message containing the outcome boolean and the description message
        """

        username = reviewRequest.usernameBeachClub
        print("Il server ha ricevuto:")
        print(username)

        filterAttributeList = []                
        filterAttributeValue = []
        if len(username) != 0:
            filterAttributeList.append('lidoId')
            filterAttributeValue.append(username)
        result = self.db.scanDb("recensioni", filterAttributeList, filterAttributeValue, 'and')
        reviews = []
        for elem in result:
            if (len(elem) > 0):
                reviews.append(grpc_pb2.reviewDetails(usernameBeachClub=elem['lidoId'], star=int(elem['valutazione']), reviewDetail=elem['titolo'], comment=elem['commento']))
        response = grpc_pb2.reviewResponse(reviews = reviews)
        return response
        

    def getAverageScoreOfBeachClub(self, reviewRequest, context):
        """ compute the average value of the reviews for the requested beach club 
    
        Args:
            reviewRequest (grpc_pb2.reviewRequest): grpc message containing the beach club username to look for
            context (_type_): 

        Returns:
            grpc_pb2.getAverageResponse: grpc message containing the average review
        """

        print("Il server ha ricevuto:")
        print(reviewRequest.usernameBeachClub)
        reviewResponse = self.getAllReviewsOfBeachClub(reviewRequest, context)
        sum=0
        counter=0
        for review in reviewResponse.reviews:
            sum = sum + review.star
            counter = counter + 1
            print(counter, ": ", review.star)
        if counter == 0:
            mean = 0.0
        else:
            mean = sum/float(counter)
        response = grpc_pb2.getAverageResponse(average = mean)
        return response
    
    def sentimentAnalysis(self, request, context):
        """ compute the sentiment analysis of the reviews related to the input city

        Args:
            request (grpc_pb2.sentimentRequest): grpc message containing the city to analyze
            context (_type_): 

        Returns:
            grpc_pb2.analysisOutput: grpc message containing a list of association (month -> list of sentiment)
        """
        
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        print('INIZIO ANALISI DEL SENTIMENTO PER {}'.format(request.city))
        city = request.city
        
        # prendo tutti i lidi della città richiesta
        accountingChannel = grpc.insecure_channel("{}:50052".format("accounting"))
        stubAccounting = grpc_pb2_grpc.AccountingStub(accountingChannel)
        list = stubAccounting.getAllBeachClubInCity(grpc_pb2.cityRequest(city=city))
        if len(list.usernameBeachClub) == 0:
            return grpc_pb2.analysisOutput(dati=[])
        
        # prendo tutte le recensioni che si riferiscono ad uno di questi lidi
        result = self.db.scanDb('recensioni', ['lidoId'], list.usernameBeachClub, 'or')

        # raggruppo tutti i commenti da analizzare
        analysisOutput = []
        
        for elem in result:
            toBreak = False
            if (len(elem) > 0):
                sentiment_output = comprehend.detect_sentiment(Text=elem['commento'], LanguageCode='it')
                print(sentiment_output)
                
                data_commento = datetime.strptime(elem['data'], "%d/%m/%Y").date()  
                data_commento_mese = data_commento.strftime("%B")
                data_commento_anno = data_commento.strftime("%Y")

                # analysisOutput = [['may 2022', ['NEG', 'POS', ...]], ...]
                for output in analysisOutput:
                    print("{}=={}?".format(output[0],"{} {}".format(data_commento_mese, data_commento_anno)))
                    
                    # se ho già un'entry che accumula tutti i sentimenti di un mese+anno
                    if output[0] == "{} {}".format(data_commento_mese, data_commento_anno):    
                        output[1].append(sentiment_output['Sentiment'])
                        toBreak = True
                        break

                if not toBreak:
                    
                    # non ho trovato nulla nella lista quindi devo aggiungere un nuovo elemento
                    new_date = "{} {}".format(data_commento_mese, data_commento_anno)
                    newList = [sentiment_output['Sentiment']]
                    output_data =  [new_date, newList]
                    analysisOutput.append(output_data)
                    toBreak = False


        dati = []
        for l in analysisOutput:
            analysisData = grpc_pb2.analysisData(mmYY=l[0], output=l[1])
            dati.append(analysisData)
        
        response = grpc_pb2.analysisOutput(dati=dati)
        return response


    
service = ReviewServicer()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_ReviewServicer_to_server(service, server)
print('Starting REVIEW SERVICE. Listening on port {}.'.format(service.port))
server.add_insecure_port('[::]:{}'.format(service.port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)