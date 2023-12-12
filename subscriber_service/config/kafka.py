import os

bootstrap_server = 'kafka0:9092' if os.environ.get('isDocker') else 'localhost:29092'

consumer_config = {
    'bootstrap.servers': bootstrap_server,
    'group.id': 'consumergroup',
    'auto.offset.reset': 'earliest'
}
