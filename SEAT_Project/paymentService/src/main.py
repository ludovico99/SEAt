from concurrent import futures
import time
import grpc
import pika
import uuid
import sqlite3
import threading
import socket


from proto import grpc_pb2
from proto import grpc_pb2_grpc

class PaymentServicer(grpc_pb2_grpc.PaymentServicer):
    
    def __init__(self):

    
        self.connectionEmail = None
        self.connectionSAGA = None
        self.channelEmail = None
        self.channelSAGA = None
        self.corr_id = None
        self.sqlConn = None

        self.establishConnectionSAGA()

        try:
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            
            with open("paymentService/createDB.sql","r") as f:
                self.sqlConn.executescript(f.read())
            self.sqlConn.commit()
        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
    

    def onlinePaymentSAGA(self, ch, method, properties, body):
        
        print("\n ONLINE PAYMENT SAGA")
        try :
            request = body.decode("utf-8").split(':')
            print("REQUEST online payment: {}".format(request))
            id = request [0]
            username = request[1]
            email = request[2]
            lido_id = request[3]
            costo = int(request[4])
            distance = float(request[5])
            budgetDifference=float(request[6])
            idCard=int(request[7])
        
            print("[Il server ha ricevuto]\nUsername:{}, lido:{}, costo:{}, distanza dal luogo richiesto: {}, differenza di prezzo dal massimo richiesto: {}".format (
            username, lido_id,costo,distance,budgetDifference,))
                    
            # 1. cerco le informazioni della carta selezionata
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
            items = self.sqlConn.execute('SELECT * FROM payment WHERE username=? AND id = ?',(username,idCard,)).fetchall()
            if len(items) == 0:
                msg = "Errore interno: non sono state trovate carte di credito corrispondenti"
                print(msg)
                return grpc_pb2.response(operationResult = False, errorMessage = msg)
   
            card = items[0][2]
            credito = items[0][4]
            print("CARTA SELEZIONATA: {}".format(card))

            # 2. cerco la carta relativa al lido
            tupleListLido = self.sqlConn.execute('SELECT * FROM payment WHERE username=?',(lido_id,)).fetchall()
            
            
            # 3. decremento il credito del cliente e aumento quello del lido
            if len(tupleListLido) != 0 and (credito>= int(costo)):
                self.sqlConn.execute("UPDATE payment SET Credito = ?  WHERE username = ? AND id = ?", (credito - int(costo), username, idCard,))
                self.sqlConn.execute("UPDATE payment SET Credito = ?  WHERE username = ?", (tupleListLido[0][4] + int(costo),lido_id, ))
                self.sqlConn.commit()
                print("Payment operation has succeded")
                request = body
                
            else:
                if len(tupleListLido) == 0:
                    errorMsg = "Lido {} selected not exists".format(lido_id)
                else: 
                    errorMsg = "Credit available isn't enough"
                request = "FAILURE:{}:{}:{}:{}".format(id,username,email,errorMsg)
            
            self.publish(request, 'History_request')

        except Exception as e:
            print (repr(e))
            errorMsg = "Payment operation has failed"
            request = "FAILURE:{}:{}:{}:{}".format(id,username,email,errorMsg)
            self.publish(request, 'History_request')
            
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
            
        
        

    def deleteCard (self, deleteReq, context):
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



    def establishConnectionEmail (self):
        try :
            self.connectionEmail = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

            self.channelEmail = self.connectionEmail.channel()

            # Dichiarazione per le code delle richieste e delle risposte
            self.channelEmail.queue_declare(queue="emailQueue")
            self.channelEmail.queue_declare(queue='responseQueue:Payment') 
            
             # BINDING DELLA CODA delle risposte all'exchange con routing key pari ad Accounting
            self.channelEmail.exchange_declare(exchange='topic_logs', exchange_type='topic')
            self.channelEmail.queue_bind(exchange='topic_logs', queue='responseQueue:Payment', routing_key="Payment.*")

                #COSA FARE ALLA RISPOSTA???
            self.channelEmail.basic_consume(
                queue='responseQueue:Payment',
                on_message_callback=self.onResponseEmail,
                auto_ack=True)

        except Exception as e:
            print(repr(e))
            return False,"Error in establishing connections and queues"
        return True,"Connection and queues are correctly established "

    def establishConnectionSAGA (self):
        try :
            self.connectionSAGA = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))


            self.channelSAGA = self.connectionSAGA.channel()

            # Dichiarazione per le code delle richieste e delle risposte
            self.channelSAGA.queue_declare(queue="Pay_request")
            self.channelSAGA.queue_declare(queue="Pay_response") 
        
            self.channelSAGA.queue_declare(queue="History_request")
            self.channelSAGA.queue_declare(queue="History_response")

            # Dichiarazione per le code delle richieste e delle risposte
            self.channelSAGA.queue_declare(queue="Account_request")
            self.channelSAGA.queue_declare(queue="Account_response")

            self.channelSAGA.queue_declare(queue="Payment_request")
            self.channelSAGA.queue_declare(queue="Payment_response")

            # #Exchange di ricezione e binding
            # self.channelSAGA.exchange_declare(exchange='topic_logs_1', exchange_type='topic')

            # self.channelSAGA.queue_bind(exchange='topic_logs_1', queue='Payment_request', routing_key="Payment.request.*")
            # self.channelSAGA.queue_bind(exchange='topic_logs_1', queue='Payment_response', routing_key="Payment.response.*")

            # #Exchange di invio
            # self.channelSAGA.exchange_declare(exchange='topic_logs_2', exchange_type='topic')       
                
            self.publishRequest = "History_request"
              
            # quando consuma da payRequest deve eseguire il pagamento
            self.channelSAGA.basic_consume(
                    queue="Pay_request",
                    on_message_callback=self.onlinePaymentSAGA,
                    auto_ack=True)

            # quando consuma da stockResponse valuta se eseguire il rollback oppure no
            self.channelSAGA.basic_consume(
                    queue="History_response",
                    on_message_callback=self.onResponseSaga,
                    auto_ack=True)


            self.channelSAGA.basic_consume(
                    queue="Payment_request",
                    on_message_callback=self.onDeleteRequest,
                    auto_ack=True)

            self.channelSAGA.basic_consume(
                    queue="Payment_response",
                    on_message_callback=self.onDeleteResponse,
                    auto_ack=True)

        except Exception as e:
            print(repr(e))
            return False,"Error in establishing connections and queues"
        return True,"Connection and queues are correctly established "

    def onResponseEmail (self,ch,method,properties,body):
        print("RESPONSE: %r:%r" % (method.routing_key, body))
        if self.connectionEmail != None:
            self.connectionEmail.close()


    def onDeleteRequest (self,ch,method,properties,body):
        try :
            list = None
            response = body.decode("utf-8").split(':')
            #request = "{}:{}".format (username,deleteReq.admin)
            print("\nPayment service has received a delete request: {}".format(response))
            username = response[0]
            admin = response[1]
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')

            list = self.sqlConn.execute('DELETE FROM payment WHERE username = ? returning *',(username,)).fetchall() 
            print(list)
            self.sqlConn.commit ()
        
            request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in payment service has succeded",list)
                            
            # self.channelSAGA.basic_publish(exchange='topic_logs_2', routing_key="Account.request.1",
            # properties=pika.BasicProperties(
            #     reply_to= "Payment_response",
            # ),
            # body=request)

            print(properties.reply_to)
            self.channelSAGA.basic_publish(exchange='', routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                reply_to= "Payment_response",
            ),
            body=request)


        except Exception as e:
            print(repr(e))
            request = "FAILURE:{}:{}:{}:{}".format(username,admin,"Delete in payment service has failed",list)
                            
            # self.channelSAGA.basic_publish(exchange='topic_logs_2', routing_key="Account.request.1", body=request)
            self.channelSAGA.basic_publish(exchange='', routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    reply_to= "Payment_response",
                ),
                body=request)

        finally:
            if self.sqlConn != None :
                self.sqlConn.close()
    
    def onDeleteResponse (self,ch,method,properties,body):
        try:
            #request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in account service has succeded",list)
            response = body.decode("utf-8").split(':')
            print("\nMessage from Payment_request: {}".format(response))
            esito = response[0]
            username = response[1]
            admin = response[2]
            msg = response[3]
            list = response[4]

            print(msg)
            if esito == "FAILURE":
                print("UNDO OPERATION in payment service is needed")
                for i in range (0,len(list)):
                    self.sqlConn.execute('INSERT INTO payment (username,cardId,cvc,Credito) values (?,?,?,?)',(list[i][0],list[i][1],list[i][2],list[i][3])).fetchall()
                    self.sqlConn.commit()


            request = "{}:{}:{}".format(username,admin,"DELETE operation completed successfully")             
            # self.channelSAGA.basic_publish(exchange='topic_logs_2', routing_key="Account.response.1", body=request)
            print(properties.reply_to)
            self.channelSAGA.basic_publish(exchange='', routing_key= properties.reply_to,
                    properties=pika.BasicProperties(reply_to = None),
            body=request)
        except Exception as e:
            print(repr(e))
        finally:
            
            if self.sqlConn != None:
                self.sqlConn.close()

            
    
    def onResponseSaga (self, ch, method, properties, body):

        try:
            response = body.decode("utf-8").split(':')
            print("\nRESPONSE Saga from History_response to Pay_response: {}".format(response))
            esito = str(response[0])
            id = int(response[1])
            username = response[2]
            email = response[3]
            lido_id = response[4]
            costo = int(response[5])
            cardId = int(response[6])
            msg = response[7]
           

            if (esito == "FAILURE"):
                self.sqlConn = sqlite3.connect('paymentService/paymentService.db')
                print("UNDO operation: modify credito")
                # 1. UNDO: aumentare il credito nella carta del cliente e diminuirlo nel lido
                self.sqlConn.execute('UPDATE payment SET Credito = Credito + ? WHERE username = ? AND id = ?', (costo, username, cardId,))
                self.sqlConn.execute("UPDATE payment SET Credito = Credito - ?  WHERE username = ?", (costo,lido_id,))

                self.sqlConn.commit()
      
                # 2. pubblicare la failure per scatenare gli altri UNDO
                request = "FAILURE:{}:{}:{}:{}".format(id,username,email,msg)
                            
            else :
                print("SENDING EMAIL")
                result, errorMsg = self.sendEmail (username, email)
                print ("result:{}, ErrorMsg:{}".format(result, errorMsg))
                request = "SUCCESS:{}:{}:{}:{}".format(id,username,email,msg)
            
            self.publish(request, 'Pay_response')

        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
        
    
    
    def publish(self, request, routingKey):
        print(request, routingKey)        
        self.corr_id = str(uuid.uuid4())
        self.channelSAGA.basic_publish(
            exchange='',
            routing_key=routingKey,
            body=request)

    def sendEmail(self, username, email):
        try :
            result = self.establishConnectionEmail ()
            if result == False:
                return False, "Error in establishing connection phase"

            request = "{}:{}#Payment".format (username,email)
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


def grpc_server(service):

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

def sagaQueueConsumer(service):
    print(" [x] Awaiting SAGA payment requests")
    service.channelSAGA.start_consuming()
    
service = PaymentServicer()
x = threading.Thread(target=grpc_server, args=(service,))
x.start()


y = threading.Thread(target=sagaQueueConsumer, args=(service,))
y.start()
x.join()




