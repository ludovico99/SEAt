from concurrent import futures
import os
import time
import grpc
import pika
import uuid
import sqlite3
import threading
import socket
from connectionSaga import ConnectionSaga


from proto import grpc_pb2
from proto import grpc_pb2_grpc

class PaymentServicer(grpc_pb2_grpc.PaymentServicer):

        self.sqlConn = None
        self.connessione = None
        self.slaves = []

        try:
            self.sqlConn = sqlite3.connect('paymentService/src/paymentService.db')
            
            with open("paymentService/src/createDB.sql","r") as f:
                self.sqlConn.executescript(f.read())
            self.sqlConn.commit()

        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()



    def deleteCard (self, deleteReq, context):
        """ perform the removal of the payment card from the microservice's local db

        Args:
            deleteReq (grpc_pb2.deleteCardRequest): grpc message that specify the card owner's username and cardId
            context (): 

        Returns:
            grpc_pb2.response: grpc message describing the outcome (operationResult, errorMessage)
        """

        print("Il server ha ricevuto:")
        print("Session: {}",deleteReq)
        username = deleteReq.username
        cardId = deleteReq.cardId
        items = self.lookupACard (username, cardId)
        try:
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            if  items == None:
                print("\nNon esistono carte di credito da eliminare")
                return grpc_pb2.response(operationResult = False, errorMessage = "There are no credit card to delete")
     
            self.sqlConn.execute('DELETE FROM payment WHERE username = ? AND cardId = ?',(username,cardId,)).fetchall() 
          
            self.sqlConn.commit ()
        except Exception as e:
            print(repr(e))
            return grpc_pb2.response(operationResult = False, errorMessage = "Delete operation has failed")
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
        response = grpc_pb2.response(operationResult = True, errorMessage = "Delete operation has succeded")
        return response


    def insertCreditCard(self, request, context):
        """Insert new credit card in the microservice's local db

        Args:
            request (grpc_pb2.creditDetails): grpc message containg the details of the card to insert
            context (): 

        Returns:
            grpc_pb2.response: grpc message describing the outcome (operationResult, errorMessage)
        """
        print("Il server ha ricevuto: ")
        print("\nusername:{}, cardId:{}, cvc:{}, credito:{}".format (request.username,request.cardId, request.cvc, request.credito))
       
        try :
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            result = self.sqlConn.execute('INSERT OR REPLACE INTO payment (username,cardId,cvc,Credito) values (?,?,?,?)',(request.username,request.cardId, request.cvc, request.credito))
            self.sqlConn.commit()
        except Exception as e:
            print(repr(e))
            return grpc_pb2.response(operationResult = False, errorMessage = "Insert operation has failed")
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
        return grpc_pb2.response(operationResult = True, errorMessage = "Insert operation has succeded")
        

    def showCards(self, request, context):
        """ get the list of card associated to user in input

        Args:
            request (grpc_pb2.session): grpc message containing the description of the user to retrieve the cards
            context (): 

        Returns:
            grpc_pb2.cardsResponse: grpc message containing the list of the cards (with details)
        """
        print("Il server ha ricevuto:")
        print("Session: {}",request)
        username = request.dict[0].value
        items = self.lookUpInDb (username)
        response = []

        if items == None:
            return grpc_pb2.cardsResponse(cards = response)

        for i in range (0,len(items)) :
            aux = list(items[i][2])
            aux[4:12]= "********"
            toShow = "".join(aux)
            print("{}) CardID:{}, CREDITO disponibile: {}".format(i+1,toShow,items[i][4]))
            response.append(grpc_pb2.cardDetails(cardId = toShow, credito=items[i][4], cvc = int(items[i][3]), id=int(items[i][0])))
        return grpc_pb2.cardsResponse(cards = response)
  

    def lookUpInDb(self, username):
        """utility function to query the local db and retrieve the list of the cards associated to the user

        Args:
            username (String): user that owns the cards

        Returns:
            List: _list of cards
        """
        try :
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            response = self.sqlConn.execute('SELECT * FROM payment WHERE username=?',(username,)).fetchall()
            print(response)     
            if len(response) == 0:
                print("No card has been inserted")
                return None

        except Exception as e:
            print(repr(e))
            print("No card has been inserted")
            return None
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
        return response

    def lookupACard(self, username, cardId):
        """ query the local db to retrieve the information associated to a specific card (with card id) of a user

        Args:
            username (String): card's owner
            cardId (String): card's identifier

        Returns:
            List: list with 1 element containing the requested card's details 
        """
        try :
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            response = self.sqlConn.execute('SELECT * FROM payment WHERE username=? AND cardId = ?',(username,cardId,)).fetchall()
            print(response)     
            if len(response) == 0:
                print("The selected card does not exist")
                return None

        except Exception as e:
            print(repr(e))
            print("An expection has been raised in searching a credit card phase")
            return None
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
        return response
    
    def updateRequest(self, request, context):
        """function to update the secondary replicas'DB in order to provide consistency

        Args:
            request (grpc_pb2.updateReq): grpc message with the details of the operation to perform
            context (): 
        Returns:
            grpc_pb2.response: grpc message describing the outcome (operationResult, errorMessage)
        """
        try:
            response = []
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')

            for updateRequest in request.o:
                op = updateRequest.op
                username =  updateRequest.username
                cardId = updateRequest.cardId
                cvc = updateRequest.cvc
                credito = updateRequest.credito
                res = None

                if op == "DELETE":
                    # elimina la entry specificata
                    res = self.deleteCard(grpc_pb2.deleteCardRequest(username = username, cardId = cardId), context)
                
                else if op == "INSERT":
                    # inserisce/aggiorna la entry specificata
                    res = self.insertCreditCard(grpc_pb2.creditDetails(username=username, cardId=cardId, cvc=cvc,credito=credito))
                
                else if op == "ADD":
                    # aggiunge il credito specificato
                    self.sqlConn.execute("UPDATE payment SET Credito = Credito + ?  WHERE username = ?", (credito , username, ))
                    self.sqlConn.commit()

                else if op == "SUB":
                    # decrementa il credito specificato
                    self.sqlConn.execute("UPDATE payment SET Credito = Credito - ?  WHERE username = ? AND id = ?", (credito, username, cardId,))
                    self.sqlConn.commit()
                else:
                    return grpc_pb2.response(operationResult = False, errorMessage = "GRPC MALFORMED")        
                
                response.append(res)
            # scandisci le entry di response, se anche una non va a buon fine torna False
            return grpc_pb2.response(operationResult = True, errorMessage = "Insert operation has succeded")
        except:
            return grpc_pb2.response(operationResult = False, errorMessage = "ERROR IN UPDATING THE REPLICAS, DATABASE COULD BE INCONSISTENT")
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()        
            
    def startConsume(self, empty, context):
        """ starts the primary replica consume for updating the db

        Args:
            uempty (grpc_pb2.empty): empty grpc message

        Returns:
            grpc_pb2.empty: empty grpc message
        """
        self.connessione = ConnectionSaga()
        y = threading.Thread(target=self.sagaQueueConsumer, args=(self.connessione,))
        y.start()
        ch = grpc.insecure_channel("{}:50055".format("payment_2"))
        self.slaves.append(grpc_pb2_grpc.PaymentStub(ch))

        
        return grpc_pb2.empty()

    def sagaQueueConsumer(self, connessione):
        """ thread that consume the incoming messages from queue

        Args:
            service (PaymentServicer): service that must consume the messages from the queue
        """
        print(" [MASTER] Awaiting SAGA payment requests")
        connessione.channel.start_consuming()
    
def grpc_server(service):
    """ thread that runs the microservice's server

    Args:
        service (PaymentServicer): service to start
    """

    try: 
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_pb2_grpc.add_PaymentServicer_to_server(service, server)
        print('Starting PAYMENT SERVICE. Listening on port 50055.')
        server.add_insecure_port('[::]:50055')
        server.start()
    except Exception as e:
        print(repr(e))
        server.stop(0)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt as e:
        print(repr(e))
        server.stop(0)

# def sagaQueueConsumer(service):
#     """ thread that consume the incoming messages from queue

#     Args:
#         service (PaymentServicer): service that must consume the messages from the queue
#     """
#     print(" [x] Awaiting SAGA payment requests")
#     service.connessione.channel.start_consuming()
    
service = PaymentServicer()
x = threading.Thread(target=grpc_server, args=(service,))
x.start()


# y = threading.Thread(target=sagaQueueConsumer, args=(service,))
# y.start()
# x.join()