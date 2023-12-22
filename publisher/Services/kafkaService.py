from confluent_kafka import Producer
from configs.kafka import server_config
import json
import sys

sys.path.append('configs/')


def delivery_callback(err, msg):
    if err:
        print(err)
    else:
        print('kafka msg sended')


def publish_news_kafka(msg, category):
    topic = f'{category}_topic'
    print(topic)
    articles = msg['articles'][:5]
    message = json.dumps(articles)

    # Create Producer instance
    p = Producer(**server_config)

    # Produce line (without newline)
    p.produce(topic, message, callback=delivery_callback)
    p.poll(1)
    p.flush()

    return True
