from flask import jsonify
from configs import config
from dotenv import load_dotenv
from Helpers.retry_helpers import exponential_backoff_retry
from flask import Flask, request

import requests
import os

app = Flask(__name__)


config_data = config.get_configs()
load_dotenv()


@exponential_backoff_retry
def get_emails_by_category(category):
    with app.app_context():
        try:
            category_url = os.getenv('CATEGORY_URL') or config_data.properties.get('CATEGORY_URL')
            print("L'url è:" + category_url + category)
            response = requests.get(category_url + category)
            if response.status_code == 200:
                data = response.json()
                if data is not None and 'emails' in data:
                    return data['emails']
                else:
                    return None
            else:
                raise requests.HTTPError(f"Error status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Si è verificato un errore durante la richiesta HTTP: {e}")
        except ValueError as e:
            print(f"Si è verificato un errore nel formato della risposta: {e}")
        except KeyError as e:
            print(f"Si è verificato un errore: {e}")
