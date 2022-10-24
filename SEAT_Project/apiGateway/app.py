from flask import Flask, render_template, redirect, request, flash, session
import grpc

from accountingGateway import AccountingGateway
from paymentGateway import PaymentGateway
from quoteGateway import QuoteGateway
from reservationGateway import ReservationGateway
from reviewGateway import ReviewGateway 
from proto import grpc_pb2
from proto import grpc_pb2_grpc
import secrets
from datetime import datetime
import locale



app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
iPAddress = "localhost"


resG = ReservationGateway()
aG = AccountingGateway ()
qG = QuoteGateway ()
pG = PaymentGateway ()
revG = ReviewGateway ()

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


########################################################################################### HOMEPAGE

@app.route('/admin', methods=('GET','POST'))
def adminHomepage():
    if request.method == "POST":
        sedie = int(request.form['sedie'])
        sdraio = int(request.form['sdraio'])
        lettini = int(request.form['lettini'])
        customer = request.form['customer']
        ombrelloni = []
        for key in request.form.keys():
            if 'x' in key:
                temp = key.split('x')
                msg = "riga: {}; colonna: {}".format(temp[0], temp[1])                
                ombrelloni.append(temp)
        
        numArray = [ombrelloni, lettini, sdraio, sedie]
        esito, msg = resG.manualReservation(session['username'], customer, numArray)
        header = ""
        if esito == True:
            header = "SUCCESSO:"
        else:
            header = "OPS ..."
        flash_msg = "{} {}".format(header, msg)
        flash(flash_msg)
        return redirect('/admin')
    data = datetime.today()
    locale.setlocale(locale.LC_TIME, "it_IT")
    giorno = data.strftime("%d")
    mese = data.strftime("%B")
    anno = data.year
    
    reservedMatrix = []
    try:
        if len(session['matrix']) == 0:
            flash('Per poter visionare il lido devi prima completare la configurazione')
        else:
            reservedMatrix = resG.getReservedSeatMatrix(session['username'], session['matrix'])
    except Exception as e:
        msg = repr(e)
        flash(msg)

    maxCol = 0
    for list in reservedMatrix:
        numCol = len(list)
        if numCol>maxCol: maxCol = numCol
    return render_template('homepageAdmin.html', giorno=giorno, mese=mese, anno=anno, maxCol=maxCol, matrix=reservedMatrix)



@app.route('/utente', methods=('GET','POST'))
def userHomepage():

    if request.method == "POST":
        suggestions = []
        details = {}
        details['username']         = session['username']
        details['type']             = session['tipoUtente']
        details['email']            = session['email']
        details['num_ombrelloni']   = request.form['num_ombrelloni']
        details['num_sdraio']       = request.form['num_sdraio']
        details['num_lettini']      = request.form['num_lettini']
        details['num_sedie']        = request.form['num_sedie']
        details['num_fila']         = request.form['num_fila']
        details['price']            = request.form['price']
        details['fromDate']         = request.form['fromDate']
        details['toDate']           = request.form['toDate']
        details['city']             = request.form['city']
        details['payOnline']        = False
        current_date = datetime.now().replace(tzinfo=None)
        format = "%Y-%m-%dT%H:%M"
        
        for key in request.form.keys():
            if key == "payOnline":
                details[key] = True
                
        try:
            fromDate = datetime.strptime(details['fromDate'], format).replace(tzinfo=None)
            toDate = datetime.strptime(details['toDate'], format).replace(tzinfo=None)
            
            if (fromDate != None and fromDate <= current_date) or (toDate != None and toDate <= current_date):
                flash("Non puoi inserire una data passata")
                return redirect('/utente')
            
            elif (toDate != None and toDate < fromDate):
                flash("La data di fine prenotazione deve essere successiva a quella iniziale")
                return redirect('/utente')
            else:                    
                details['fromDate'] = fromDate
                details['toDate'] = toDate
                suggestions = resG.getSuggestions(details)  
                
        except Exception as e:
            flash("Fallimento nell'inserimento delle date")
            print(repr(e))
            return redirect('/utente')

        session['form_detail'] = details
        session['suggestions'] = suggestions
        return redirect('/utente/offerte')
    return render_template('homepageUser.html')




########################################################################################### RECENSIONI

@app.route('/admin/recensioni', methods=('GET','POST'))
def adminRecensioni():
    media=0
    recensioni = revG.getReviews(session['username'])
    if len(recensioni) != 0:
        media = revG.getAverage(session['username'])
    return render_template('recensioniAdmin.html', reviews=recensioni, avg=media)

@app.route('/utente/recensioni', methods=('GET','POST'))
def utenteRecensioni():
    recensioni = revG.getReviews("")
    return render_template('recensioniUser.html', reviews=recensioni)


@app.route('/utente/nuova_recensione', methods=('GET','POST'))
def utenteNuovaRecensione():

    if request.method == "POST":
        lidoID          = request.form['lido_id']
        valutazione     = int(request.form['stelle'])
        commento        = request.form['commento1']
        commento_lungo  = request.form['commento2']
        esito, msg = revG.postReview(lidoID, valutazione, commento, commento_lungo)
        header = create_header(esito)
        flash_msg = "{} {}".format(header, msg)
        flash(flash_msg)
        return redirect('/utente/nuova_recensione')
    return render_template('nuova_recensioneUser.html')




########################################################################################### ACCOUNT


@app.route('/admin/accounting', methods=('GET','POST'))
def accountingAdmin():
    return render_template('accountingAdmin.html', username=session['username'])


@app.route('/admin/accounting/configurazione_lido', methods=('GET','POST'))
def configureBeachClub():
    if request.method == "POST":
        num_sedie = int(request.form['num_sedie'])
        num_file = int(request.form['num_file'])
        num_sdraio = int(request.form['num_sdraio'])
        num_lettini = int(request.form['num_lettini'])
        
        numInRow = []   # (numfila1, num fila2, ...)
        for i in range (0, num_file):
            key = 'numInRow'+str(i+1)
            numInRow.append(int(request.form[key]))
        session['matrix'] = numInRow
        
        response, msg = aG.changeConfiguration(num_file, num_lettini, num_sdraio, num_sedie, numInRow, session['username'], session['tipoUtente'], session['email'])
        flash (msg)
        return redirect('/admin/accounting/configurazione_lido')
    return render_template('accounting_configurazione.html')


@app.route('/admin/accounting/credenziali', methods=('GET','POST'))
def configureCredentials():
    if request.method == "POST":
        new_password = request.form['new_password']
        new_email = request.form['new_email']
        new_name = request.form['new_name']
        new_place = request.form['new_place']
        new_card = request.form['new_card']
        response,msg = aG.changeAccountCredentials(True, new_password, new_email, new_name, new_place, new_card, session['username'], session['email'])
        if response == True:
            session['username'] = new_name
            session['tipoUtente'] = True
            session['email'] = new_email
        flash (msg)
        return redirect('/admin/accounting/credenziali')
    return render_template('accounting_accountAdmin.html')


@app.route('/admin/accounting/credenziali/elimina', methods=('GET','POST'))
def deleteAccountAdmin():
    if request.method == "POST":
        aG.deleteAccount(session['username'], admin=True)
        return redirect('/')
    return render_template('accounting_accountAdmin.html')


@app.route('/admin/accounting/prezzi', methods=('GET','POST'))
def configurePrices():
    if request.method == "POST":

        priceOmbrellone = int(request.form['costo_ombrellone'])
        priceSdraio = int(request.form['costo_sdraio'])
        priceLettino = int(request.form['costo_lettino'])
        priceSedia = int(request.form['costo_sedia'])
        incrPrimeFile = int(request.form['incRow'])
        incrAltaStagione = int(request.form['incAltaStagione'])
        incrBassaStagione = int(request.form['incBassaStagione'])
        incrMediaStagione = int(request.form['incMediaStagione'])

        qG.modifyPrice(priceOmbrellone, priceSdraio, priceLettino, priceSedia, incrPrimeFile, incrAltaStagione, incrBassaStagione, incrMediaStagione, session['username'])
        return redirect('/admin/accounting/prezzi')
    return render_template('accounting_priceAdmin.html')

@app.route('/utente/accounting', methods=('GET','POST'))
def accountingUser():
    return render_template('accountingUser.html', username=session['username'])

@app.route('/utente/accounting/credenziali', methods=('GET','POST'))
def configureUserCredentials():
    if request.method == "POST":
        new_password = request.form['new_password']
        new_email = request.form['new_email']
        response = aG.changeAccountCredentials(False, new_password, new_email, None, None, None, session['username'], session['email'])        
        if response == True:
            session['tipoUtente'] = False
            session['email'] = new_email
        flash("Credenziali aggiornate!")   

        return redirect('/utente/accounting/credenziali')
    return render_template('accounting_accountUser.html')


@app.route('/utente/accounting/credenziali/elimina', methods=('GET','POST'))
def deleteAccountUser():
    if request.method == "POST":
        result = aG.deleteAccount(session['username'], admin=False)
        if result == True:
            return redirect('/')
        else:
            flash('eliminazione fallita')
            return redirect('/utente/accounting/credenziali/elimina')
    return render_template('accounting_accountUser.html')


@app.route('/utente/accounting/listaCarte', methods=('GET','POST'))
def showCards():
    cards = pG.listOfCards(session['username'],session["email"],session['tipoUtente'])
    return render_template('accounting_cardListUser.html', cards = cards)


@app.route('/utente/accounting/carte', methods=('GET','POST'))
def configureCards():
    if request.method == "POST":
        username = session['username']
        cardId = str(request.form['new_card_number'])
        cvc = str(request.form['new_cvc'])
        if 'Elimina' in request.form:
            cardId = request.form['new_card_number']
            response = pG.deleteCard(session['username'],cardId)
            if response == True:
                flash("Card has been deleted correctly")
            else :
                flash("Selected card does not exist")
            return redirect('/utente/accounting/carte')
        else:
            credito = int(request.form['new_credit'])
            response = pG.insertCreditCard (username,cardId,cvc,credito)
            if response == True:
                flash("Card has been modified")
            else :
                flash("Selected card does not exist")
            return redirect('/utente/accounting/carte')
    return render_template('accounting_cardUser.html')

    

########################################################################################### LOGIN E REGISTRAZIONE


@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == "POST":
        username = request.form['user']
        password = request.form['pwd']

        accountingChannel = grpc.insecure_channel("{}:50052".format(iPAddress))
        stubAccounting = grpc_pb2_grpc.AccountingStub(accountingChannel)

        sessione = stubAccounting.login(grpc_pb2.loginRequest(username=username, password=password))
        
        if len(sessione.dict) == 0:
            flash("login fallito, riprovare con altre credenziali")
            return redirect('/login')

        try:                                                    #0: username; 1: tipoUtente; 2: email
            session['username'] = sessione.dict[0].value
            session['tipoUtente'] = sessione.dict[1].value
            session['email'] = sessione.dict[2].value
            
            if sessione.dict[1].value == "True":
                
                response = stubAccounting.getMatrix(grpc_pb2.reviewRequest(usernameBeachClub = session['username']))
                matrix = []
                for i in response.numInRow:
                    matrix.append(i)
                session['matrix'] = matrix
                return redirect('/admin')
            else :
                return redirect('/utente')
        except Exception as e:
            flash(repr(e))
            flash("login fallito, riprovare con altre credenziali")
            return redirect('/login')
    return render_template('login.html')


@app.route('/registrazione', methods=('GET','POST'))
def newAccount():

    if request.method == "POST":
        username = request.form['user']
        password = request.form['pwd']
        email = request.form['email']
        admin = request.form['admin']
        details=[False,False,False,False,False]

        if admin == "2":
            adminBool = False
            beachClubName = location = cardId = None
            cvc = 0
        else:
            adminBool = True
            beachClubName = request.form['lido']
            location = request.form['locazione']
            cardId = request.form['numero_carta']
            cvc = request.form['cvc']
                
            for key in request.form.keys():
                if key == "ristorazione":
                    details[0] = True
                if key == "bar":
                    details[1] = True
                if key == "campi":
                    details[2] = True
                if key == "animazione":
                    details[3] = True
                if key == "palestra":
                    details[4] = True
            
        res, flash_string = aG.newAccount(username, password, email, adminBool, beachClubName, location, cardId,cvc, details)
        flash(flash_string)
        return redirect('/registrazione')
    return render_template('registrazione.html')


########################################################################################### PRENOTAZIONE


@app.route('/utente/offerte/<int:idx>', methods=('GET','POST'))
def selectedOffer(idx):
    
    if request.method == "POST":
        suggestions = session['suggestions']
        
        if session['form_detail']['payOnline']==True:
            session['selected_proposal'] = suggestions[idx]
            return redirect('/utente/offerte/pagamento')
        else:
            esito, msg = resG.reserve(session['form_detail'], suggestions[idx], '0')
            header = create_header(esito)
            flash_msg = "{} {}".format(header, msg)
            flash(flash_msg)
            return redirect('/utente')
    return render_template('offerteUser.html', suggestions = session['suggestions'])


@app.route('/utente/offerte', methods=('GET','POST'))
def listOffers():
    return render_template('offerteUser.html', suggestions = session['suggestions'])


@app.route('/utente/offerte/pagamento', methods=('GET','POST'))
def cardRequest():
    if request.method == "POST":
        cardId = '0'
        found = False
        for key in request.form.keys():
            print(key)
            if 'selectedNum'==key:
                found = True
                cardId = request.form['selectedNum']
                esito, msg = resG.reserve(session['form_detail'], session['selected_proposal'], cardId)
                header = create_header(esito)
                flash_msg = "{} {}".format(header, msg)
                flash(flash_msg)
        if found == False:
            return redirect('/utente')
        
        return redirect('/utente')
    cards = pG.listOfCards(session['username'],session["email"],session['tipoUtente'])
    return render_template('cardRequest.html', cards = cards)


########################################################################################### SENTIMENT ANALYSIS


@app.route('/utente/analisi_del_sentimento', methods=('GET','POST'))
def analysisRequest():
    
    if request.method == "POST":
        city = request.form['luogo']
        session['labels'], session['barChartDataset'], session['count'] = revG.analyze(city)
        return redirect('/utente/analisi_del_sentimento/{}'.format(city))
    return render_template('sentimentAnalysisForm.html')


@app.route('/utente/analisi_del_sentimento/<string:city>', methods=('GET','POST'))
def analysis(city):
    return render_template('sentimentAnalysis.html', city=city, nPositive=session['count'][3], nNegative=session['count'][0], nMixed=session['count'][1], nNeutral=session['count'][2], labels=session['labels'], dataset=session['barChartDataset'])


########################################################################################### CARTE


@app.route('/admin/pagamenti', methods=('GET','POST'))
def payment():
    result = pG.listOfCards(session['username'],session["email"],session['tipoUtente'])
    return render_template('paymentCardAdmin.html', cards = result)


def create_header(esito):
    if esito == True:
        header = "SUCCESSO:"
    else:
        header = "OPS ..."
    return header


app.run()