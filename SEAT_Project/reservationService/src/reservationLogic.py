from dBUtils import DBUtils
from datetime import datetime

class ReservationLogic (object):
    def __init__(self):
        self.db = DBUtils()


    def totOmbrelloni(self, lidoId):
        """ get the number of seats (umbrella) of the input beach club

        Args:
            lidoId (string): beach club username

        Returns:
            int: seats
            string: outcome message
        """
        
        try:
            data = self.db.scanDb('postazioniPerFila', ['lidoId'], lidoId)

            if len(data) == 0:
                print("No seats available")
                return None, "No seats available" 
                
            tot = 0
            for i in range (0, len(data)):
                tot += data[i]['nOmbrelloni']
            return tot, "Lookup in postazioni has succeded"

        except Exception as e:
            print(repr(e))
            return None, "Exception in lookup postazioni"


    def totPezzi(self, lidoId):
        """ get the number of deckchairs, beach loungers and chairs of the input beach club

        Args:
            lidoId (string): beach club username

        Returns:
            dictionary: contains the number for each requested item
            string: outcome message
        """
        try:
            totPezzi = {'totaleSdraio':0,'totaleLettini':0 ,'totaleSedie':0 }
            data = self.db.scanDb('dettagliLido', ['username'], [lidoId])   
                                
            if len(data) == 0:
                return None, "No items available"
            
            totPezzi['totaleSdraio'] = int(data[0]['totaleSdraio'])
            totPezzi['totaleLettini'] = int(data[0]['totaleLettini'])
            totPezzi['totaleSedie'] = int(data[0]['totaleSedie'])
            return totPezzi, "Lookup in magazzino has succeded"

        except Exception as e:
            print(repr(e))
            return None, "{} non ha ancora completato la configurazione, riprova più tardi".format(lidoId)
    

    def totaleOmbrelloniPerFila (self,lidoId, nFila):
        """ get the number of seats that the requested beach club has in the specified row

        Args:
            lidoId (string): beach club id
            nFila (string): row

        Returns:
            int: number of seats
            string: outcome message
        """
        try:
            data = self.db.scanDb('postazioniPerFila', ['lidoId', 'numeroFila'], [lidoId, nFila])

            if len(data) == 0:
                print("No seats available")
                return None, "No seats available" 
    
            return int(data[0]['nOmbrelloni']), "Lookup in postazioni per fila has succeded"

        except Exception as e:
            print(repr(e))
            return None, "Exception in lookup postazioni per fila"

    
    def getReservations (self, lidoId, date, nFila):
        """ get the reserved seats for a date in the beach club's requested row

        Args:
            lidoId (string): beach club username
            date (datetime.datetime): reservation's date
            nFila (int): row

        Returns:
            list(string): list of reservations id
            list(int): list of reserved seats in the specified row
            dictionary: dictionary containing the number of items not available in the date
            string: outcome message
        """

        response = []
        ombrelloniOccupati = []
        pezziOccupati = {'sdraioOccupate':0,'lettiniOccupati' :0,'sedieOccupate':0}
        try:
            # 1. Cerco tutte le prenotazioni per un lido
            data = self.db.scanDb('prenotazione', ['lidoId'], [lidoId])
            if data == None:
                msg = "Errore nella richiesta al database"
                print(msg)
                # return  grpc_pb2.response(operationResult = False, errorMessage = msg)
                return None, None, None, msg
            
            if(len(data) == 0):
                return response, ombrelloniOccupati,pezziOccupati, "No Reservations available"

            for i in range(0, len(data)):                  
                
                # 2. Incremento il numero di sdraio occupate se la prenotazione su cui sto iterando comprende la data odierna
                fromDate = datetime.strptime(data[i]['fromDate'], "%d/%m/%Y").date()  
                toDate = datetime.strptime(data[i]['toDate'], "%d/%m/%Y").date()

                if (date <= toDate and date >= fromDate):
                    
                    pezziOccupati['sdraioOccupate'] = pezziOccupati['sdraioOccupate'] + int(data[i]['nSdraio'])
                    pezziOccupati['lettiniOccupati'] = pezziOccupati['lettiniOccupati'] + int(data[i]['nLettini'])
                    pezziOccupati['sedieOccupate'] = pezziOccupati['sedieOccupate'] +  int(data[i]['nSedie'])
                    
                    temp = (data[i]['ombrelloneId']).split('x')
                    fila = int(temp[0])
                    posto = int(temp[1])

                    # 3. Se incontro una prenotazione per la fila che sto cercando la inserisco tra gli ombrelloni occupati
                    if fila == nFila:
                        response.append(data[i]['prenotazioneId'])
                        ombrelloniOccupati.append(posto)
                        
            return response,ombrelloniOccupati,pezziOccupati, "Lookup in postazioni has succeded"

        except Exception as e:
            print(repr(e))
            return None, None, None, "Exception in lookup resevations"
