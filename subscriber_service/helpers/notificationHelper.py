from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import TransactionalEmailsApi, CreateSmtpEmail, SendSmtpEmail, SendSmtpEmailSender

import json

with open('configs/config.json') as config_file:
    config_data = json.load(config_file)

SENDGRID_API_KEY = config_data.get('SENDINBLUE_API_KEY')
# PASS ProgettoDSBDSEND
SENDER = config_data.get('SENDER_MAIL')

api_instance = TransactionalEmailsApi()

# Configura l'header con l'API Key
api_instance.api_client.configuration.api_key['api-key'] = SENDGRID_API_KEY


def send_email(receiver, category, title, link):
    stili_inline = '''
        <style>
            /* Stili per il corpo email */
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
            a:hover {
                text-decoration: underline;
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
    corpo_email = f'''
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Nuovo articolo nella categoria "{category}"</title>
            {stili_inline}
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
        html_content=corpo_email
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("Email inviata con successo! ID:", response.message_id)
    except ApiException as e:
        print("Errore durante l'invio dell'email:", e)
