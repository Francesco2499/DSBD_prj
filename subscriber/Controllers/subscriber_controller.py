from flask import jsonify
from Services import kafkaService

import threading
import sys

sys.path.append("Services/")


def subscribe_category(category):
    topic_name = f'{category}_topic'

    try:
        thread = threading.Thread(target=kafkaService.subscribe_to_topic, args=(topic_name,))
        thread.start()

        print("Starting subscribe!")
        return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})
    except kafkaService.TopicNotFoundException as e:
        return jsonify({'success': False, 'error': f'Topic {topic_name} not found: {str(e)}'}), 404

    except kafkaService.KafkaConnectionError as e:
        return jsonify({'success': False, 'error': f'Error connecting to Kafka: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': f'Error subscribing to {category} topic: {str(e)}'}), 500
