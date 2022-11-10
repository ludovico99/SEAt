# How-to di SEAt
How-to basato su distribuzione Linux Ubuntu/Debian

[INSTALLAZIONE]:

1) Eseguire il clone del repository github:

        git clone https://github.com/ludovico99/SEAt.git

[CONFIGURAZIONE]:

1) Installare AWS cli sulla macchina host:

    1) Installare AWS CLI:

            sudo apt install awscli

    2) Iniziare l'AWS CLI configuration fornendo i dettagli in AWS details:
    
            aws configure 

    Per Inserire le stringhe fornite in Learner Lab - Foundational Services --> AWS details:
    ![AWS details](/immagini/AWS_details.png)
    Viene creato il file seguente ~/.aws/credentials. 

    3) Questo file va aggiornato ogni volta che viene avviata una nuova sessione del learner lab.
    E' presente lo script SEAT_project/credentials.sh che permette di copiare le nuove credenziali di sessione in  ~/.aws/credentials e in tutte le cartelle dei microservizi (Questo perchè nel dockerfile che ha visibilità "locale" viene eseguito il comando COPY che copia il contenuto di credentials della macchina host nel file root/.aws/credentials del container che esponde il servizio). 

    Il deploy dell'applicazione è basato sull'utilizzo  di:

    --> terraform: E' un open-source IaC tool software che consente di creare in modo sicuro e predicibile, cambiare e migliorare l'infrastruttura, nel nostro caso EC2. E' basato sulla dichiarazione di risorse AWS 

    --> ansible: E' un software libero che consente di automatizzare le procedure di configurazione e gestione sui sistemi unix-like e Windows

2) E' necessario installare entrambi i tools (tutorial per ubuntu/debian):

    --> Terraform: 

        curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
        sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
        sudo apt install terraform

    --> Ansible:

        python3 -m pip install --user ansible
        python3 -m pip install --upgrade --user ansible

 3) E' necessario modificare i files SEAT_Project/terraform/terraform.tfvars e /SEAT_Project/deploy.yaml per configurare rispettivamente terraform e ansible:

    --> Per terraform è possibile modificare il tipo di istanza da creare, l'ami dell'istanza EC2 (Utilizzare distribuzioni Ubuntu/Debian)  da creare, l'id del security group (Deve necessariamente garantire l'ingresso a traffico HTTP e SSH proveniente dalla macchina dalla quale si intende fare il deploy. In uscita è importante che venga garantito il passaggio a traffico HTTP) e il nome della chiave privata (creata in precedenza all'interno del servizio EC2. Vedere https://docs.aws.amazon.com/it_it/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

    --> Per ansible è possibile fare la copia dell'application directory decommentando le righe da 13 a 17 e modificando la variabile local_app_dir. 

 4) In SEAT_Project/startup.sh è necessario specificare il path assoluto della chiave privata .pem e della directory del progetto

 5) Fare la stessa cosa del punto 4 nel file SEAT_Project/deploy.sh

[ESECUZIONE]:

1) Eseguire lo script bash /SEAT_Project/startup.sh per istanziare in modo automatico l'istanza EC2, le tabelle di dynamoDB e la coda del servizio SQS --> Il comando precedente porta alla creazione/modifica del file hosts.ini con l'indirizzo ip della macchina EC2 appena creata. Questo file verrà utilizzato da ansible.

        bash SEAT_Project/startup.sh

2) Aspettare che l'istanza EC2 sia in esecuzione 

3) Eseguire lo script SEAT_Project/deploy.sh per eseguire la copia della directory attraverso protocollo scp e per eseguire il deploy in ansible. Attraverso ansible verrà installato docker sulla macchina remota e l'applicazione verrà installata come systemd service.

        bash SEAT_Project/deploy.sh

4) Arrestare l'istanza EC2 e riavviarla. 

5) L'applicazione sarà in esecuzione su http://[indirizzo ip publico della macchina]:80



