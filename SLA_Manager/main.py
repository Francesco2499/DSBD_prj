from flask import Flask
from prometheus_api_client import PrometheusConnect

app = Flask(__name__)

prometheus_url = 'http://prometheus:9090'
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)


@app.route('/prova', methods=['GET'])
def create_customer():
    result = prom.custom_query(query='container_cpu_usage_seconds_total')
    print(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)
