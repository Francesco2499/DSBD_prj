from confluent_kafka import Consumer
from configs.kafka import consumer_config
from Helpers import subscriber_helpers

import json
import sys

sys.path.append("Helpers/")


def subscribe_to_topic(topic_name):
    try:
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
            print("Waiting for message!")
            articles = msg.value().decode('utf-8')
            result = subscriber_helpers.handle_response(articles, topic_name)
            print('Received message: {}'.format(articles))
            print(result)

        consumer.close()
    except KeyboardInterrupt:
        print("Process interrupted by user")

    except json.JSONDecodeError as e:
        print(f'Error in JSON parsing: {str(e)}')

    except Exception as e:
        print(f'Unexpected error: {str(e)}')

    return
