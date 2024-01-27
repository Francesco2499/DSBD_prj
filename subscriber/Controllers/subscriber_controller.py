from flask import jsonify
from Services import kafka_service
from configs import config
from confluent_kafka.admin import AdminClient
from configs.kafka import bootstrap_server
import threading
import sys
import time

sys.path.append("Services/")
sys.path.append("configs/")
sys.path.append("Helpers/")

config_data = config.get_configs()


def check_kafka_topics_existence():
    topics = ["general_topic", "sports_topic", "science_topic", "technology_topic"]

    try:
        with AdminClient({'bootstrap.servers': bootstrap_server}) as admin_client:
            # Verifica la connessione a Kafka
            metadata = admin_client.list_topics(timeout=10)
            existing_topics = metadata.topics

            # Verifica la presenza dei topic specificati
            for topic in topics:
                if topic not in existing_topics:
                    print(f"Il topic {topic} non esiste in Kafka.")
                    return False

    except Exception as e:
        print(f"Errore durante il controllo dei topic su Kafka: {e}")
        return False

    return True


def subscribe_category():
    while not check_kafka_topics_existence():
        print('Kafka topics not already created')
        time.sleep(1)

    categories_str = config_data.properties.get('categories')
    print(categories_str)
    categories_list = categories_str.split(',')
    for category in categories_list:
        topic_name = f'{category}_topic'
        print("Il topic è :" + topic_name)
        try:
            thread = threading.Thread(target=kafka_service.subscribe_to_topic, args=(topic_name,))
            thread.start()

            print("Starting subscribe!")
            print(jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'}))
            time.sleep(2)

        except Exception as e:
            return jsonify({'success': False, 'error': f'Error subscribing to {category} topic: {str(e)}'}), 500

    return jsonify({'success': True})
