from flask import jsonify
from Services import kafka_service, news_service
from configs import config

import time
import sys

sys.path.append("Services/")
sys.path.append("configs/")

config_data = config.get_configs()


def get_news_by_category():
    categories_str = config_data.properties.get('categories')
    print(categories_str)
    categories_list = categories_str.split(',')
    for cat in categories_list:
        print("Get news for category: " + cat)
        try:
            response = news_service.get_news(cat)
            if response.status_code == 200:
                print('Response is ok')
                news_data = response.json()
                result = kafka_service.publish_news_kafka(news_data, cat)

                if result.json['Success']:
                    print(result.json['Message'])
                else:
                    return result.json['Message']
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    return jsonify({'success': True, 'Message':'Publisher finished!'})