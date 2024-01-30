# News Norifier APP

## Descrizione

Il progetto proposto si focalizza sulla progettazione e implementazione di un sistema di distribuzione di notizie informative, mirando a ottimizzare l'esperienza degli utenti attraverso l'utilizzo di microservizi.
L'applicativo simula un ecosistema di distribuzione di notizie in cui gli utenti possono iscriversi e specificare le loro preferenze di categoria. Contemporaneamente, il sistema è in grado di recuperare notizie da un servizio esterno come NewsAPI, filtrando le richieste in base a delle categorie specifiche che avranno una corrispondenza con le categorie selezionate dagli utenti. Questo processo consente al sistema di notificare gli utenti in modo personalizzato, garantendo un flusso di informazioni rilevante e di loro interesse. Per fare ciò si è utilizzato un sistema architetturale del tipo Publisher-Subscriber, facendo uso della tecnologia offerta da Kakfa.

## Prerequisiti
- [Docker](https://docs.docker.com/)
- [Kubernetes](https://kubernetes.io/docs/home/)
- ApiKey del servizio [NewsAPI](https://newsapi.org/)
- ApiKey del servizio [SendInBlue](https://account-app.brevo.com/)

## Installazione su Docker

Se desideri eseguire l'applicazione utilizzando Docker in un ambiente locale, segui questi passaggi:

1. **Clona il repository:**

    ```bash
    git clone https://github.com/Francesco2499/DSBD_prj.git
    cd DSBD_prj
    ```

2. **Creare un file .env da inserire all'interno della folder del subscriber**
    
    ```bash
    notepad /DSBD_prj/subscriber/.env
    # Inserire URL completo per contattare il Category Service e ottenere le email data una categoria con key -> CATEGORY_URL
    # Inserire l'API KEY generata per utilizzare SendInBlue con key -> SENDINBLUE_API_KEY
    # Salvare la modifica
    ```

3. **Build delle immagini Docker:**

    ```bash
    # Esegui il build delle immagini per tutti i servizi
    docker-compose build
    ```

4. **Esegui i container Docker:**

    ```bash
    docker-compose up -d
    ```

## Installazione Kubernetes

1. **Clona il repository:**

   ```bash
   git clone https://github.com/Francesco2499/DSBD_prj.git
   ```

2. **Inserire il valore dell'ApiKey nella configurazione  Subscriber**
    - All'interno del file deployment.yaml, trovare la configurazione del Subscriber.
    - Andare a sostituire la stringa 'Insert your apikey' con la chiave generarata per utilizzare SendInBlue

3. **Configurazione del Cluster Kubernetes:**

   Assicurati di avere un cluster Kubernetes funzionante. Puoi utilizzare strumenti come Minikube.

4. **Applica i Manifesti Kubernetes:**

   ```bash
   kubectl apply -f deployment.yaml
   ```

5. **Accesso ai Servizi:**

   - L'API Gateway è esposto tramite un servizio LoadBalancer. Esegui il comando seguente per ottenere l'indirizzo IP esterno:

     ```bash
     kubectl get service apigateway-service
     ```
    Usando Minikube è possibile lanciare il seguente comando per riuscire a comunicare con il servizio.

     ```bash
     minikube tunnel
     ```
    Link utili: https://minikube.sigs.k8s.io/docs/start/
   
   - Per ottenere altri indirizzi relativi ai servizi di monitoraggio delle metriche eseguire:
   
    ```bash
     minikube service slamanager-service --url
     minikube servuce prometheus-service --url
     minikube service cadvisor-service --url
     ```

## Utilizzo

L'applicazione è ora in esecuzione sul tuo cluster Kubernetes. Puoi interagire con i diversi servizi attraverso le loro rispettive API. Per informazioni dettagliate sull'utilizzo di ciascun servizio, consulta la documentazione dei singoli componenti e la collection Postman fornita.

Per effettuare un test dell'applicativo:
- Importare la collection di API su Postman.
- Cercare nella collection all'interno della folder **APIGW - Customer Service** l'endpoint "**Create Customer**", inserendo nome, password ed email desiderate ed effettuare la chiamata.
- All'interno della stessa folder, effettuare una chiamata all'endpoint Auth per la generazione del token, inserendo email e password già registrate.  Uno script si assicurerà di inserire il token in una variabile d'ambiente.
- Accedere alla folder **APIGW - Category Service** ed effettuare una chiamata ad "**ADD Category**" in cui bisognerà specificare come nome della categoria almeno uno tra i seguenti:
    - general
    - sports
    - science
    - technology
- Sempre nella stessa folder chiamare l'endpoint"**ADD CAtegory Preference**". Qui bisogna specificare la mail (con cui ci si è registrati e autenticati) e la categoria scelta come preferenza. Il token sarà già inserito grazie alla variabile d'ambiente già definita.
- A questo punto se il publisher è in modalità test, accedere alla folder Publisher Service ed effettuare una chiamata all'endpoint 'Publish News' altrimeni attendere la normale schedulazione.
- Attendere e verificare la ricezione delle e-mail di notifica nella propria casella di posta
