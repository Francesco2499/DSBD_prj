from confluent_kafka import Consumer
from configs.kafka import consumer_config
from helpers import subscriberHelpers
import json
import sys

sys.path.append("helpers/")

def subscribe_to_topic(topic_name):
    try:
        print(topic_name)
        consumer_config['group.id'] = f'{topic_name}_group'
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic_name])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            try:
                print("Waiting for notify!")
                articles = msg.value().decode('utf-8')
                subscriberHelpers.handle_response(articles, topic_name)
                print('Received message: {}'.format(articles))

            except json.JSONDecodeError as e:
                print(f'Errore durante il parsing del JSON: {str(e)}')

        consumer.close()
    except Exception as e:
        print(e)

    return



