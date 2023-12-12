from confluent_kafka import Consumer, KafkaException
from config import kafka as kafka_configs
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

valid_access_tokens={}


def subscribe_to_topic(topic_name):
    try:
        kafka_configs.consumer_config['group.id'] = f'{topic_name}_group'
        consumer = Consumer(kafka_configs.consumer_config)
        consumer.subscribe([topic_name])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print(f'Received message from {topic_name}: {msg.value().decode("utf-8")}')

        consumer.close()
    except Exception as e:
        print(f'Exception in subscribing to {topic_name}: {str(e)}')

@app.route('/subscribe', methods=['GET'])
def subscribe_to_chosen_topic():
    try:
        access_token = request.headers.get('Authorization')  # Ottieni il token di accesso dall'header Authorization
        if access_token in valid_access_tokens.values():
            category = request.args.get('category', 'general')  # Se non specificata, default a 'news'
            topic_name = f'{category}_topic'

            thread = threading.Thread(target=subscribe_to_topic, args=(topic_name,))
            thread.start()

            return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})
        else:
            return jsonify({'success': False, 'error': 'Authentication failed'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
