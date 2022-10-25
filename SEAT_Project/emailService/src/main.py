import pika


class EmailService (object):

    def __init__(self):
        try :
            #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.connectionSAGA = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq:5672'))

            self.channel = self.connection.channel()

            #CODA PER LE RICHIESTE PROVENIENTI DALL'ACCOUNT
            result = self.channel.queue_declare(queue='emailQueue')
            self.requestQueue = result.method.queue

            self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
            
            self.channel.basic_consume(
                queue=self.requestQueue,
                on_message_callback=self.onRequest,
                auto_ack=True)

        except Exception as e:
            print(repr(e))
            self.errorMsg = "Error in establishing connections and queues"
    
    def onRequest(self,ch,method,props,body):
        if props.correlation_id != None :
            print("REQUEST: %r:%r" % (props.correlation_id, body))
            #TODO SEND EMAIL
            tokens = str(body).split('#')
            toQueue = tokens[-1][:-1]
            print (tokens[-1][:-1])
            message = "EMAIL has been sent to {}".format(str(body))
            if toQueue == "Accounting":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Accounting.response", body=message)
            elif toQueue == "Reservation":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Reservation.response", body=message)
            elif toQueue == "Payment":
                self.channel.basic_publish(exchange='topic_logs', routing_key="Payment.response", body=message) 

        

emailService = EmailService()
print("Starting EMAIL SERVICE. [x] Awaiting email requests")
emailService.channel.start_consuming()