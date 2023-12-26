import requests
from flask import jsonify

NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
NEWS_API_KEY = 'b67fa3203a504b90bd2f6297ff8aab73'


def get_news(category):
    try:
        params = {
            'country': 'it',
            'apiKey': NEWS_API_KEY,
            'category': category
        }

        response = requests.get(NEWS_API_URL, params=params)

        if response.status_code == 200:
            return response
        else:
            return jsonify({'success': False, 'error': f"Error in request: {response.status_code}"})
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': f"Connection error: {str(e)}"})
    except Exception as e:
        return jsonify({'success': False, 'error': f"Generic error: {str(e)}"}), 500

