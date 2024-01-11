from flask import jsonify
from configs import config
from Helpers.retry_helpers import exponential_backoff_retry

import requests
import sys
import os

sys.path.append('configs/')
sys.path.append('Helpers/')

configs = config.get_configs()


@exponential_backoff_retry
def get_news(category):
    try:
        params = {
            'country': 'it',
            'apiKey': os.getenv('NEWS_API_KEY') or configs.properties.get('NEWS_API_KEY'),
            'category': category
        }

        news_url = os.getenv('NEWS_URL') or configs.properties.get('NEWS_URL')
        print(news_url)
        response = requests.get(news_url, params=params)

        if response.status_code == 200:
            return response
        else:
            return jsonify({'success': False, 'error': f"Error in request: {response.status_code}"})
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': f"Connection error: {str(e)}"})
    except Exception as e:
        return jsonify({'success': False, 'error': f"Generic error: {str(e)}"}), 500

