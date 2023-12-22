from flask import jsonify
from Services import kafkaService

import threading
import sys

sys.path.append("Services/")


def subscribe_category(category):
    try:
        print(category)
        topic_name = f'{category}_topic'
        thread = threading.Thread(target=kafkaService.subscribe_to_topic, args=(topic_name,))
        thread.start()
        print("starting subscribe!")
        return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
