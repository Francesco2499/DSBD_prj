from confluent_kafka import Consumer, KafkaException
from configs.kafka import consumer_config
from . import notificationHelper
import json


def subscribe_to_topic(topic_name):
    try:
        consumer_config['group.id'] = f'{topic_name}_group'
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic_name])

        # togli _topic
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            try:
                articles = msg.value().decode('utf-8')
                print('Received message: {}'.format(articles))
                # Decodifica il payload JSON in un oggetto Python
                articles = json.loads(msg.value().decode('utf-8'))
                # cerca user che hanno {topic_name} senza _topic e chiama notification helper
                category = topic_name.replace("_topic", "")
                notificationHelper.send_email('24maggio1999@gmail.com', category, articles['title'], articles['url'])
            except json.JSONDecodeError as e:
                print(f'Errore durante il parsing del JSON: {str(e)}')

        consumer.close()
    except Exception as e:
        print(e)

    return
