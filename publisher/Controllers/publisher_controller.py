from configs import constants
from flask import jsonify
from ..Services import kafkaService, newsService

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

                    if result:
                        print('Published news for category:' + cat)
                    else:
                        print('Error in publish news for category:' + cat)
                        # controlla Exception di Kafka
                    time.sleep(120)
                    return
                else:
                    return jsonify({'success': False, 'error': 'Failed to fetch news data'}), 500
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
