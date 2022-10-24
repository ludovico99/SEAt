import grpc

from proto import grpc_pb2
from proto import grpc_pb2_grpc
import datetime

class ReviewGateway():

    def __init__(self):
        self.reviewChannel = grpc.insecure_channel("{}:50054".format("localhost"))
        self.stubReview = grpc_pb2_grpc.ReviewStub(self.reviewChannel)

    def getReviews(self,lidoID):
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
        response = self.stubReview.getAverageScoreOfBeachClub(grpc_pb2.reviewRequest(usernameBeachClub = lidoID))
        return response.average


    def postReview(self,lidoID, valutazione, commento, commento_lungo):     
        response = self.stubReview.review(grpc_pb2.reviewDetails(
            usernameBeachClub = lidoID, 
            star= valutazione, 
            reviewDetail = commento, 
            comment = commento_lungo
        ))
        return response.operationResult, response.errorMessage
    
    def analyze(self,location):
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