from confluent_kafka import Producer
from config import kafka as kafka_config
from flask import jsonify
def delivery_callback(err, msg):
    if err:
        print(err)
    else:
        print('kafka msg sended')

def sendKafkaMessage(topic, msg):
    # Create Producer instance
    p = Producer(**kafka_config.server_config)

    # Produce line (without newline)
    p.produce(topic, msg, callback=delivery_callback)
    p.poll(1)
    p.flush()

    return True
