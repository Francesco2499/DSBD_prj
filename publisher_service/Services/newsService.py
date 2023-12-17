import requests
from flask import jsonify
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'  # Cambia con l'URL reale
NEWS_API_KEY = 'b67fa3203a504b90bd2f6297ff8aab73'  #

def get_news(cat):
    try:
        params = {
            'country': 'it',  # Cambia con il paese di interesse
            'apiKey': NEWS_API_KEY,
            'category': cat
        }

        response = requests.get(NEWS_API_URL, params=params)

        return response
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
