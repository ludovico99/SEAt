from connection import Connection
from proto import grpc_pb2
from proto import grpc_pb2_grpc
from connectionEmail import ConnectionEmail
import uuid
import pika
import sqlite3

class ConnectionSaga (Connection):
    def __init__(self, slaves):
        self.sqlConn = None
        self.establishConnection()
        self.slaves = slaves


    def publish(self, request, routingKey):
        """Utility function to publish a message in the specified queue

        Args:
            request (String): body of the message to publish
            routingKey (String): name of queue to publish the message
        """
        print (request, routingKey)        
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=routingKey,
            body=request)



    def on_channel_open (self):
        """Define request and response queues

        Returns:
            BOOL: outcome of the definition, True if succeded
        """
        try:
            print("CHANNEL CORRECTLY CREATED")
            
            # Dichiarazione per le code delle richieste e delle risposte per PRENOTAZIONE+PAGAMENTO
            self.channel.queue_declare(queue="Pay_request")
            self.channel.queue_declare(queue="Pay_response") 
        
            self.channel.queue_declare(queue="History_request")
            self.channel.queue_declare(queue="History_response")

            # Dichiarazione per le code delle richieste e delle risposte per DELETE ACCOUNT
            self.channel.queue_declare(queue="Account_request")
            self.channel.queue_declare(queue="Account_response")

            self.channel.queue_declare(queue="Payment_request")
            self.channel.queue_declare(queue="Payment_response") 
            
            # quando consuma da Pay_request cerca di effettuare il pagamento
            self.channel.basic_consume(
                    queue="Pay_request",
                    on_message_callback=self.onlinePaymentSAGA,
                    auto_ack=True)
            
            # quando consuma da History_response valuta se eseguire o no il rollback del PAGAMENTO
            self.channel.basic_consume(
                    queue="History_response",
                    on_message_callback=self.onResponseSaga,
                    auto_ack=True)

            # quando consuma da Payment_request cerca di effettuare l'eliminazione della carta di credito
            self.channel.basic_consume(
                    queue="Payment_request",
                    on_message_callback=self.onDeleteRequest,
                    auto_ack=True)

            # quando consuma da Payment_response valuta se eseguire o no il rollback della DELETE
            self.channel.basic_consume(
                    queue="Payment_response",
                    on_message_callback=self.onDeleteResponse,
                    auto_ack=True)

            return True

        except Exception as e:
            print(repr(e))
            if (self.connection != None):
                self.connection.close()
            return False


    def onlinePaymentSAGA(self, ch, method, properties, body):
        """ CALLBACK FUNCTION: perform the payment moving credit from customer card to lido's card.
        If the payment fails trigger the reservation's UNDO, else trigger the update of the user history.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
        
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
                routingKey = 'History_request'
                
            else:
                if len(tupleListLido) == 0:
                    errorMsg = "Lido {} selected not exists".format(lido_id)
                else: 
                    errorMsg = "Credit available isn't enough"
                request = "FAILURE:{}:{}:{}:{}".format(id,username,email,errorMsg)
                routingKey = 'Pay_response'
            
            self.publish(request, routingKey)

        except Exception as e:
            print (repr(e))
            errorMsg = "Payment operation has failed"
            request = "FAILURE:{}:{}:{}:{}".format(id,username,email,errorMsg)
            self.publish(request, 'Pay_response')
            
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
    
    def onResponseSaga (self, ch, method, properties, body):
        """ CALLBACK FUNCTION: evaulate (and potentially perform) the ROLLBACK of the payment.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """

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
                request = "SUCCESS:{}:{}:{}:{}".format(id,username,email,msg)

                # 3. aggiornare le repliche se l'operazione ha avuto successo
                for stub in self.slaves:
                    todo = []
                    todo.append(grpc_pb2.operation(op="ADD", username=lido_id, cardId="", cvc=0, credito=costo))
                    todo.append(grpc_pb2.operation(op="SUB", username=username, cardId=str(cardId), cvc=0, credito=costo))
                    res = stub.updateRequest(grpc_pb2.updateReq(o=todo))
                    print("ho aggiornato la replica secondaria")
                    #TODO se res è falso??? magari memorizza le info e fai l'undo dell'operazione
            
            self.publish(request, 'Pay_response')

        except Exception as e:
            print(repr(e))
        finally:
            if self.sqlConn != None:
                self.sqlConn.close()
    
    def onDeleteRequest (self,ch,method,properties,body):
        """ CALLBACK FUNCTION: try to delete the payment card.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
        try :
            list = None
            response = body.decode("utf-8").split(':')
            print("\nPayment service has received a delete request: {}".format(response))
            username = response[0]
            admin = response[1]
            self.sqlConn = sqlite3.connect('paymentService/paymentService.db')

            list = self.sqlConn.execute('DELETE FROM payment WHERE username = ? returning *',(username,)).fetchall() 
            print(list)
            self.sqlConn.commit ()
        
            request = "SUCCESS:{}:{}:{}:{}".format(username,admin,"Delete in payment service has succeded",list)

            print(properties.reply_to)

            self.channel.basic_publish(exchange='', routing_key="Account_request",
            properties=pika.BasicProperties(
                reply_to= "Payment_response",
            ),
            body=request)


        except Exception as e:
            print(repr(e))
            request = "FAILURE:{}:{}:{}:{}".format(username,admin,"Delete in payment service has failed",list)
                            
            # self.channel.basic_publish(exchange='topic_logs_2', routing_key="Account.request.1", body=request)
            self.channel.basic_publish(exchange='', routing_key="Account_request",
                properties=pika.BasicProperties(
                    reply_to= "Payment_response",
                ),
                body=request)

        finally:
            if self.sqlConn != None :
                self.sqlConn.close()
    

    def onDeleteResponse (self,ch,method,properties,body):
        """ CALLBACK FUNCTION: evaluate (and potentially perform) the ROLLBACK of payment card's removal.

        Args:
            ch (pika.channel.Channel): channel
            method (pika.spec.Basic.Deliver):
            properties (pika.spec.BasicProperties): properties associated to message consumed
            body (bytes): message consumed
        """
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

            else:
                # aggiornare le repliche se l'operazione ha avuto successo
                for stub in self.slaves:
                    todo = []
                    for i in range (0,len(list)):
                        todo.append(grpc_pb2.operation(op="DELETE", username=list[i][0], cardId=list[i][1], cvc=int(list[i][2]), credito=int(list[i][2])))
                    
                    res = stub.updateRequest(grpc_pb2.updateReq(o=todo))
                    print("ho aggiornato la replica secondaria")
                    #TODO se res è falso??? magari memorizza le info e fai l'undo dell'operazione
            
            request = "{}:{}:{}".format(username,admin,"DELETE operation completed successfully")             
            # self.channel.basic_publish(exchange='topic_logs_2', routing_key="Account.response.1", body=request)
            print(properties.reply_to)
            self.channel.basic_publish(exchange='', routing_key= properties.reply_to,
                properties=pika.BasicProperties(
                    reply_to = None
                ),
                body=request)
        except Exception as e:
            print(repr(e))
        finally:
            
            if self.sqlConn != None:
                self.sqlConn.close()

    
    