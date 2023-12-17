import os

host = 'kafka0:9092' if os.environ.get('isDocker') else 'localhost:29092'
server_config = {'bootstrap.servers': host}
