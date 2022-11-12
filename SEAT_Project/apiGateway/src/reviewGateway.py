import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc
import time
import datetime

class ReviewGateway():

    def __init__(self):
        self.ch = grpc.insecure_channel("{}:50057".format("service_registry"))
        self.stubServiceRegistry = grpc_pb2_grpc.ServiceRegistryStub(self.ch) 
        while (True):
            
            try:  
                response = self.stubServiceRegistry.getPortAndIp(grpc_pb2.registryRequest(serviceName= "ReviewServicer"))
                break
            except Exception as e:

                time.sleep(5)

        if response == None or response.responses[0].port == "0":
            print("{}:Unable to contact service registry: static binding needed to continue".format(self.__class__.__name__))
            self.reviewChannel = grpc.insecure_channel("{}:{}".format("review","50054"))
            self.stubReview = grpc_pb2_grpc.ReviewStub(self.reviewChannel) 


        else :
            print("{}:Service registry successfully contacted: dynamic binding available".format(self.__class__.__name__))
            self.reviewChannel = grpc.insecure_channel("{}:{}".format(response.responses[0].hostname,response.responses[0].port))
            self.stubReview = grpc_pb2_grpc.ReviewStub(self.reviewChannel) 

    def getReviews(self,lidoID):
        """entry point for the retrieve of all the reviews related to the beach club in input. If lidoID is "" then
        the function will look for all the review in the database.

        Args:
            lidoID (String): username of the beach club to look for or the empty string.

        Returns:
            List: list of reviews. Each element is a list containing: average score, review title, review comment
        """
        getAllReviews = False
        if lidoID == "":
            getAllReviews = True
       
        print("sto richiedendo ", lidoID)
        response = self.stubReview.getAllReviewsOfBeachClub(grpc_pb2.reviewRequest(usernameBeachClub = lidoID))
        recensioni = []
        if len(response.reviews) != 0:
            for i in response.reviews:
                r = []
                r.append(i.star)
                print(i.star)
                r.append(i.reviewDetail)
                r.append(i.comment)
                recensioni.append(r)
                if(getAllReviews):
                    r.append(i.usernameBeachClub)
        return recensioni

    def getAverage(self,lidoID):
        """entry point for the retrieve of the selected beach club's average score

        Args:
            lidoID (String): username of the beach club to look for

        Returns:
            float: average score
        """
        response = self.stubReview.getAverageScoreOfBeachClub(grpc_pb2.reviewRequest(usernameBeachClub = lidoID))
        return response.average


    def postReview(self,lidoID, valutazione, commento, commento_lungo):     
        """entry point for the insertion of a new review in the database

        Args:
            lidoID (String): username of the beach club reviewed
            valutazione (int): number in the interval[1;5] representing the evaluation of the beach club
            commento (String): comment title
            commento_lungo (String): detailed comment

        Returns:
            _type_: _description_
        """
        response = self.stubReview.review(grpc_pb2.reviewDetails(
            usernameBeachClub = lidoID, 
            star= valutazione, 
            reviewDetail = commento, 
            comment = commento_lungo
        ))
        return response.operationResult, response.errorMessage
    
    def analyze(self,location):
        """entry point for the SENTIMENT ANALYSIS: retrieve the sentiment of the visitors of a place

        Args:
            location (String): city to analyze 

        Returns:
            List: list of the labels of the chart (month-year)
            List: list of the values for the plot
            List: each value is the total count of Positive Sentiment (or Negative, or Mixed, or Neutral)
        """
        response = self.stubReview.sentimentAnalysis(grpc_pb2.sentimentRequest(city=location))

        dataset = {}
        for dato in response.dati:
            valori = []
            for sentimento in dato.output:
                valori.append(sentimento)
            dataset[dato.mmYY] = valori
        orderedDict =  dict(sorted(dataset.items(), key=lambda k: datetime.datetime.strptime(k[0], "%B %Y"), reverse=False))
        
        barChartDataset = [[],[],[],[]]
        countSentiment = [0,0,0,0]
        labels = []
        for key in orderedDict:
            cp=0
            cng=0
            cneu=0
            cm=0
            for sentimento in orderedDict[key]:
                if sentimento=="POSITIVE": 
                    countSentiment[3] = countSentiment[3]+1
                    cp=cp+1
                elif sentimento=="NEGATIVE": 
                    countSentiment[0] = countSentiment[0]+1
                    cng = cng +1
                elif sentimento=="MIXED": 
                    countSentiment[1] = countSentiment[1]+1
                    cm = cm+ 1
                elif sentimento=="NEUTRAL": 
                    countSentiment[2]= countSentiment[2]+1
                    cneu = cneu +1
            labels.append(key)
            barChartDataset[0].append(cng)
            barChartDataset[1].append(cm)
            barChartDataset[2].append(cneu)
            barChartDataset[3].append(cp)

        
        return labels, barChartDataset, countSentiment