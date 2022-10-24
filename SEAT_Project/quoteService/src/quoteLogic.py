from datetime import datetime, timedelta

class QuoteLogic (object):
    
    def __init__(self):
        # calcola i periodi di bassa, media e alta stagione 
        now = datetime.now()
        month = now.month
        year = now.year
        if month>=9 and month<=12:
            year = year +1
        inizioAltaStagione = datetime(year, 8, 1)
        inizioBassaStagione = datetime(year, 9, 1)
        inizioMediaStagione = datetime(year, 7, 1)
        self.inizioStagione=[]
        self.inizioStagione.append(inizioBassaStagione)
        self.inizioStagione.append(inizioMediaStagione)
        self.inizioStagione.append(inizioAltaStagione)
    

    def dayInEachSeason(self, fromDate, toDate):
        """ get the number of days touched in each season from a date to another

        Args:
            fromDate (datetime.datetime): start date
            toDate (datetime.datetime): end date

        Returns:
            dictionary: each key is a season and is associated with the number of days touched
        """
        
        stagioni = {}
        fromSeason = self.whichSeason(fromDate)
        toSeason = self.whichSeason(toDate)

        # calcolo il numero di stagioni in cui voglio prenotare
        stagioniAttraversate = abs((toSeason-fromSeason)%3+1)
                   
        giorniTotali = (toDate - fromDate).days
        if giorniTotali>90:
            print("non puoi prenotare per più di 90 giorni. La tua prenotazione era di giorni ", giorniTotali)
            return None
        
        for i in range(0, stagioniAttraversate):
            s = (fromSeason-1+i)%3  #rappresenta l'indice quindi parte da 0
            
            # fase 1: settaggio delle date di inizio e fine stagione
            y = self.inizioStagione[s].year
            if(s==0 and i==0 and (fromDate.year==y-1 or fromDate<self.inizioStagione[(s+1)%3])):
                m = self.inizioStagione[s].month
                d = self.inizioStagione[s].day
                dataInizioStagione = datetime(y-1,m,d)

            else:
                dataInizioStagione = self.inizioStagione[s]
            # print("data inizio stagione ", dataInizioStagione)


            y = self.inizioStagione[(s+1)%3].year
            print(dataInizioStagione.year)
            if(s==0 and i == stagioniAttraversate-1 and dataInizioStagione.year == y):
                m = self.inizioStagione[(s+1)%3].month
                d = self.inizioStagione[(s+1)%3].day
                dataFineStagione = datetime(y+1,m,d)
                # print("sono qui, ", dataFineStagione)
            else:
                dataFineStagione = self.inizioStagione[(s+1)%3]
                # print("qui pt2, ", dataFineStagione)

            # fase 2: calcolo delle date iniziali e finali della prenotazione nella stagione corrente

            if fromDate >= dataInizioStagione and fromDate < dataFineStagione:
                dataInizialeNellaStagione = fromDate
            else:
                dataInizialeNellaStagione = dataInizioStagione
            # print("data iniziale nella stagione:", dataInizialeNellaStagione)
                
            if toDate >= dataInizioStagione and toDate < dataFineStagione:
                dataFinaleNellaStagione = toDate
            else:
                dataFinaleNellaStagione = self.inizioStagione[(s+1)%3] - timedelta(days=1)
            # print("data finale nella stagione:", dataFinaleNellaStagione)

            deltaT = dataFinaleNellaStagione.replace(hour=0, minute=0) - dataInizialeNellaStagione.replace(hour=0, minute=0)
            # print("Prenotazione:", (deltaT.days+1), "giorni nella stagione ", s+1)
            stagioni.update({str(s+1):deltaT.days+1})

        return stagioni


    def whichSeason(self, date):
        """ get the season to which the specified date belongs. 

        Args:
            date (datetime.datetime): date

        Returns:
            int: low season (1); medium season (2); high season (3)
        """
        
        if date >= self.inizioStagione[1] and date < self.inizioStagione[2]:
            return 2
        elif date >= self.inizioStagione[2] and date < self.inizioStagione[0]:
            return 3
        else:
            return 1