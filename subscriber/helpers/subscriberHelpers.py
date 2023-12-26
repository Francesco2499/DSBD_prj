from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import TransactionalEmailsApi, SendSmtpEmail, SendSmtpEmailSender
from Services import categoryService
from flask import jsonify

import json
import sys

sys.path.append("Services/")

with open('configs/config.json') as config_file:
    config_data = json.load(config_file)

SENDGRID_API_KEY = config_data.get('SENDINBLUE_API_KEY')
SENDER = config_data.get('SENDER_MAIL')
# PASS ProgettoDSBDSEND
# cambia APIKEY e sender
api_instance = TransactionalEmailsApi()
api_instance.api_client.configuration.api_key['api-key'] = SENDGRID_API_KEY


def handle_response(msg, topic_name):
    articles = json.loads(msg)
    print("Update in ", topic_name)
    category = topic_name.replace("_topic", "")
    response = categoryService.get_emails_by_category(category)
    if response is not None and 'emails' in response:  # Verifica se il campo "emails" è presente nella risposta
        email_list = response['emails']
        if email_list is not None:  # Ottieni la lista di email
            for email in email_list:
                print("Sending mail to:", email)
                for article in articles:
                    print(article['title'])
                receiver = email or SENDER
                send_email(receiver, category, articles)

            return jsonify({"Message:", "All users notified!"})
        else:
            return jsonify({"Message:", "There are not users with category preference:", category})


def send_email(receiver, category, articles):
    num_articles = len(articles)
    style = get_style_for_email()

    html_articles = get_info_by_articles(articles)

    htmlEmail = f'''
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Nuovo articolo nella categoria "{category}"</title>
            {style}
        </head>
        <body>
            <div class="container">
                <h1>Trovati nuovi articoli per la categoria {category}</h1>
                <p>Sono stati aggiunti {num_articles} nuovi articoli:</p>
                {html_articles}
            </div>
        </body>
        </html>
    '''

    send_smtp_email = SendSmtpEmail(
        sender=SendSmtpEmailSender(email=SENDER),
        to=[{"email": receiver}],
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


def get_style_for_email():
    return '''
         <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 80%;
                margin: 20px auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            h1 {{
                color: #333;
            }}
            p {{
                color: #666;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    '''


def get_info_by_articles(articles):
    articles_html = ""

    for item in articles:
        title = item["title"]
        link = item["link"]
        article_block = f'''
            <p><strong>Titolo:</strong> <a href="{link}">{title}</a></p>
        '''
        articles_html += article_block

    return articles_html
