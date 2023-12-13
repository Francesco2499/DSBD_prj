from confluent_kafka import Consumer, KafkaException
from ..config import kafka as kafka_configs


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