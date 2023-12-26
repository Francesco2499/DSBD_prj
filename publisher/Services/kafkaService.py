from confluent_kafka import Producer, KafkaException
from configs.kafka import server_config
from flask import jsonify
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

    try:
        # Create Producer instance
        p = Producer(**server_config)

        # Produce line (without newline)
        p.produce(topic, message, callback=delivery_callback)
        p.poll(1)
        p.flush()

        return jsonify({"Success": True, "Message": 'Published news for category:' + category})
    except KafkaException as kafka_exception:
        return jsonify({"Success": False, "Message": f"Kafka Exception while publishing: {kafka_exception}"})
    except Exception as e:
        return jsonify({"Success": False, "Message": f"Unexpected error while publishing: {e}"})
