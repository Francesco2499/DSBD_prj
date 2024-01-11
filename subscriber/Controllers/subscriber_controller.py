from flask import jsonify
from Services import kafka_service
from configs import config

import threading
import sys
import time

sys.path.append("Services/")
sys.path.append("configs/")
sys.path.append("Helpers/")

config_data = config.get_configs()


def subscribe_category():
    categories_str = config_data.properties.get('categories')
    print(categories_str)
    categories_list = categories_str.split(',')
    for category in categories_list:
        topic_name = f'{category}_topic'
        print("Il topic è :" + topic_name)
        try:
            thread = threading.Thread(target=kafka_service.subscribe_to_topic, args=(topic_name,))
            thread.start()

            print("Starting subscribe!")
            print(jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'}))
            time.sleep(2)

        except Exception as e:
            return jsonify({'success': False, 'error': f'Error subscribing to {category} topic: {str(e)}'}), 500

    return jsonify({'success': True})
