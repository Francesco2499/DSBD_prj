from configs import constants
from flask import jsonify
from Services import kafkaService, newsService

import time
import sys

sys.path.append("Services/")
sys.path.append("configs/")


def get_news_by_category():
    while True:
        for cat in constants.category:
            print("Get news for category: " + cat)
            try:
                response = newsService.get_news(cat)
                if response.status_code == 200:
                    print('Response is ok')
                    news_data = response.json()
                    result = kafkaService.publish_news_kafka(news_data, cat)

                    if result.Success:
                        print(result.Message)
                    else:
                        return result.Message
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500

