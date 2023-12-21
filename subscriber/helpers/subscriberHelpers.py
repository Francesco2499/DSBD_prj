from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import TransactionalEmailsApi, SendSmtpEmail, SendSmtpEmailSender
from ..Services import categoryService
import requests
import json
import sys

with open('configs/config.json') as config_file:
    config_data = json.load(config_file)

SENDGRID_API_KEY = config_data.get('SENDINBLUE_API_KEY')
SENDER = config_data.get('SENDER_MAIL')
# PASS ProgettoDSBDSEND
# cambia APIKEY e sender
api_instance = TransactionalEmailsApi()
api_instance.api_client.configuration.api_key['api-key'] = SENDGRID_API_KEY


def handle_response(msg, topic_name):
    articles = json.loads(msg.value().decode('utf-8'))
    category = topic_name.replace("_topic", "")
    response = categoryService.get_emails_by_category(category)
    if 'emails' in response:  # Verifica se il campo "emails" è presente nella risposta
        email_list = response['emails']  # Ottieni la lista di email
        for email in email_list:
            notify_users(email, category, articles)
        return "Tutti gli utenti sono stati notificati!"


def notify_users(receiver, category, articles):
    title = articles['title']
    link = articles['url']
    receiver = receiver or "24maggio1999@gmail.com"
    send_email(receiver, category, title, link)


def send_email(receiver, category, title, link):
    style = '''
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 80%;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            h1 {
                font-size: 28px;
                color: #333333;
                margin-bottom: 15px;
            }
            p {
                font-size: 16px;
                color: #666666;
                margin-bottom: 10px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 15px;
                background-color: #007bff;
                color: #ffffff;
                border-radius: 5px;
                text-decoration: none;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
    '''

    # Costruzione del corpo dell'email con HTML
    htmlEmail = f'''
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Nuovo articolo nella categoria "{category}"</title>
            {style}
        </head>
        <body>
            <div class="container">
                <h1>Nuovo articolo nella categoria "{category}"</h1>
                <p>È stato aggiunto un nuovo articolo:</p>
                <p><strong>Titolo:</strong> {title}</p>
                <a href="{link}" class="button">Leggi l'articolo</a>
            </div>
        </body>
        </html>
    '''

    send_smtp_email = SendSmtpEmail(
        sender=SendSmtpEmailSender(email=SENDER),
        to=[{"email": SENDER}],
        subject=f'Nuovo articolo nella categoria "{category}"',
        html_content=htmlEmail
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("Email inviata con successo! ID:", response.message_id)
    except ApiException as e:
        print("Errore durante l'invio dell'email:", e)
    except ConnectionError as conn_error:
        print("Errore di connessione durante l'invio dell'email:", conn_error)
    except TimeoutError as timeout_error:
        print("Timeout durante l'invio dell'email:", timeout_error)
    except Exception as ex:
        print("Errore generico durante l'invio dell'email:", ex)
