from confluent_kafka import Producer
from config import kafka as kafka_config, constants
from flask import Flask, jsonify
from helpers import kafkaHelpers

import requests
import json

app = Flask(__name__)
producer = Producer(**kafka_config.server_config)

NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'  # Cambia con l'URL reale
NEWS_API_KEY = 'b67fa3203a504b90bd2f6297ff8aab73'  # Inserisci la tua chiave API


@app.route('/publish_news', methods=['POST'])
def publish_news():
    for cat in constants.category:
        result = get_news_by_category(cat)


def get_news_by_category(category):
    try:
        params = {
            'country': 'it',  # Cambia con il paese di interesse
            'apiKey': NEWS_API_KEY
        }
        response = requests.get(NEWS_API_URL, params=params)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data['articles'][:5]  # Prendiamo solo le prime 5 notizie
            result = False
            for article in articles:
                # Creare il messaggio da pubblicare su Kafka
                message = json.dumps(article)
                topic = f'{category}_topic'  # Utilizzare la categoria per creare il topic corrispondente

                # Pubblicazione del messaggio sul topic specificato su Kafka
                result = kafkaHelpers.sendKafkaMessage(topic, message)

            if result:
                return jsonify({'success': True, 'message': 'News published successfully'})
            else:
                return jsonify({'success': False, 'error': 'Failed to publish news data'}), 500
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch news data'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
