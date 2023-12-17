from flask import jsonify
from ..Services import kafkaService

import threading


def subscribe_category(category):
    try:
        topic_name = f'{category}_topic'
        thread = threading.Thread(target=kafkaService.subscribe_to_topic, args=(topic_name,))
        thread.start()
        return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
