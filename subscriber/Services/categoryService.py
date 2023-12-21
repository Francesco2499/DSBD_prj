from flask import jsonify
import requests


def get_emails_by_category(category):
    try:
        response = requests.get('http://localhost:8082/categories/preferences?category_name' + category)
        if response.status_code == 200:
            data = response.json()  # Converte la risposta JSON in un dizionario Python
            if 'emails' in data:  # Verifica se il campo "emails" è presente nella risposta
                return data['emails']
            else:
                return jsonify({"error": "Il campo 'emails' non è presente nella response JSON"})
        else:
            raise requests.HTTPError(f"Error status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Si è verificato un errore durante la richiesta HTTP: {e}")
    except ValueError as e:
        print(f"Si è verificato un errore nel formato della risposta: {e}")
    except KeyError as e:
        print(f"Si è verificato un errore: {e}")