# News Norifier APP

## Descrizione

Il progetto proposto si focalizza sulla progettazione e implementazione di un sistema di distribuzione di notizie informative, mirando a ottimizzare l'esperienza degli utenti attraverso l'utilizzo di microservizi.
L'applicativo simula un ecosistema di distribuzione di notizie in cui gli utenti possono iscriversi e specificare le loro preferenze di categoria. Contemporaneamente, il sistema è in grado di recuperare notizie da un servizio esterno come NewsAPI, filtrando le richieste in base a delle categorie specifiche che avranno una corrispondenza con le categorie selezionate dagli utenti. Questo processo consente al sistema di notificare gli utenti in modo personalizzato, garantendo un flusso di informazioni rilevante e di loro interesse. Per fare ciò si è utilizzato un sistema architetturale del tipo Publisher-Subscriber, facendo uso della tecnologia offerta da Kakfa.

## Prerequisiti
- Docker
- Kubernetes
- ApiKey del servizio NewsAPI

## Installazione su Docker

Se desideri eseguire l'applicazione utilizzando Docker in un ambiente locale, segui questi passaggi:

1. **Clona il repository:**

    ```bash
    git clone https://github.com/Francesco2499/DSBD_prj.git
    ```

2. **Build delle immagini Docker:**

    ```bash
    # Esegui il build delle immagini per tutti i servizi
    docker-compose build
    ```

3. **Esegui i container Docker:**

    ```bash
    docker-compose up -d
    ```

## Installazione Kubernetes

1. **Clona il repository:**

   ```bash
   git clone https://github.com/Francesco2499/DSBD_prj.git
   ```

2. **Configurazione del Cluster Kubernetes:**

   Assicurati di avere un cluster Kubernetes funzionante. Puoi utilizzare strumenti come Minikube.

3. **Applica i Manifesti Kubernetes:**

   ```bash
   kubectl apply -f deployment.yaml
   ```

4. **Accesso ai Servizi:**

   - L'API Gateway è esposto tramite un servizio LoadBalancer. Esegui il comando seguente per ottenere l'indirizzo IP esterno:

     ```bash
     kubectl get service apigateway-service
     ```
    Usando Minikube è possibile lanciare il seguente comando per riuscire a comunicare con il servizio.

     ```bash
     minikube tunnel
     ```

   - Per ottenere altri indirizzi relativi ai servizi di monitoraggio delle metriche eseguire:
   
    ```bash
     kubectl get service slamanager-service
     kubectl get service prometheus-service
     kubectl get service cadvisor-service
     ```

## Utilizzo

L'applicazione è ora in esecuzione sul tuo cluster Kubernetes. Puoi interagire con i diversi servizi attraverso le loro rispettive API. Per informazioni dettagliate sull'utilizzo di ciascun servizio, consulta la documentazione dei singoli componenti e la collection Postman fornita.
