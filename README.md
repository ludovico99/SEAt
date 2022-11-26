# How-to di SEAt
How-to basato su distribuzione Linux Ubuntu/Debian

### INDICE: 
- INSTALLAZIONE: ottenere la copia locale del codice
- PREREQUISITI: dettagli sull'installazione di AWS CLI, Terraform e Ansible. Saltare se già installati
- CONFIGURAZIONE: dettagli per eseguire il codice
- ESECUZIONE: istruzioni per l'avvio dell'applicazione                                          




## INSTALLAZIONE

1) Eseguire il clone del repository github:

        git clone https://github.com/ludovico99/SEAt.git
        

## PREREQUISITI

1) Installare AWS cli sulla macchina host:

    1) Installare AWS CLI:

            sudo apt install awscli

    2) Iniziare l'AWS CLI configuration fornendo i dettagli in AWS details:
    
            aws configure 
            
        Inserire le stringhe fornite in Learner Lab - Foundational Services --> AWS details:
        
        ![AWS details](/immagini/AWS_details.png)
        
    3) Viene creato il file ~/.aws/credentials: va aggiornato ogni volta che viene avviata una nuova sessione del learner lab.
    E' presente lo script SEAT_project/credentials.sh che permette di copiare le nuove credenziali di sessione in  ~/.aws/credentials. In questo file deve essere indicato il path assoluto del progetto.


    
2) Il deploy dell'applicazione è basato sull'utilizzo  di Terraform e Ansible. Per installarli su ubuntu/debian seguire gli step:

    1) Terraform: 

            curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
            sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
            sudo apt install terraform

    2) Ansible:

            python3 -m pip install --user ansible
            python3 -m pip install --upgrade --user ansible



## CONFIGURAZIONE

1) Modificare i files:

    * TERRAFORM (file: SEAT_Project/terraform/terraform.tfvars) - è possibile modificare:
      - il tipo di istanza da creare, 
      - l'ami dell'istanza EC2 (Utilizzare distribuzioni Ubuntu/Debian) da creare, 
      - l'id del security group (Deve necessariamente garantire l'ingresso a traffico HTTP e SSH proveniente dalla macchina dalla quale si intende fare il deploy. In uscita è importante che venga garantito il passaggio a traffico HTTP),
      - il nome della chiave privata (creata in precedenza all'interno del servizio EC2. Vedere https://docs.aws.amazon.com/it_it/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

    * ANSIBLE (file: /SEAT_Project/deploy.yaml) - è possibile fare la copia dell'application directory decommentando le righe da 13 a 17 e modificando la variabile local_app_dir. 

2) Specificare in SEAT_Project/startup.sh il path assoluto della chiave privata .pem e della directory del progetto

3) Fare la stessa cosa del punto 2 nel file SEAT_Project/deploy.sh

4) Modificare la variabile d'ambiente SCALE_FACTOR nel file SEAT_project/run.sh per configurare il numero di repliche per il servizio pagamento.




## ESECUZIONE

1) Istanziare in modo automatico l'istanza EC2, le tabelle di dynamoDB e la coda del servizio SQS. Il comando porta alla creazione/modifica il file hosts.ini (utilizzato da Ansible) con l'indirizzo ip della macchina EC2 appena creata.

        bash SEAT_Project/startup.sh

2) Attendere il passaggio di "verifica dello stato" da "inizializzazione in corso" a "2/2 controlli superati"

3) Eseguire la copia della directory attraverso protocollo scp e successivamente il deploy in ansible. Viene installato docker sulla macchina remota e l'applicazione viene installata come systemd service.

        bash SEAT_Project/deploy.sh

4) Arrestare l'istanza EC2 e riavviarla. 

5) Attendere qualche minuto (circa 8) per consentire il download delle librerie.

6) L'applicazione sarà in esecuzione su http://[indirizzo ip publico della macchina]:80.

NB: Ad ogni arresto e riavvio dell'istanza EC2 l'indirizzo IP pubblico associato viene cambiato.



