from flask import Flask, request, jsonify
import requests
from config import get_configs
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
config = get_configs()

# URL del customer service
CUSTOMER_URL = os.getenv('CUSTOMER_URL') or config.properties.get('CUSTOMER_URL')
CATEGORY_URL = os.getenv('CATEGORY_URL') or config.properties.get('CATEGORY_URL')
PUBLISHER_URL = os.getenv('PUBLISHER_URL') or config.properties.get('PUBLISHER_URL')
SUBSCRIBER_URL = os.getenv('SUBSCRIBER_URL') or config.properties.get('SUBSCRIBER_URL')


@app.route('/api/<string:service>/<string:subpath>', methods=['GET', 'POST'])
def forward_requests(service, subpath):
    # Componi l'URL completo del servizio sottostante
    if service == 'customers':
        if subpath:
            service_endpoint = f"{CUSTOMER_URL}/{subpath}"
        else:
            service_endpoint = f"{CUSTOMER_URL}"
    elif service == 'categories':
        if subpath:
            service_endpoint = f"{CATEGORY_URL}/{subpath}"
        else:
            service_endpoint = f"{CATEGORY_URL}"
    # only for test
    elif service == 'publisher':
        service_endpoint = f"{PUBLISHER_URL}"
    else:
        return jsonify({"error": f"Route for service: {service} not defined"}), 404
    # Inoltra la richiesta al servizio
    headers = request.headers  # Passa tutti gli header originali
    params = request.args      # Passa tutti i parametri della query originali
    if request.method == 'GET':
        response = requests.get(service_endpoint, headers=headers, params=params)
    elif request.method == 'POST':
        response = requests.post(service_endpoint, headers=headers, params=params, json=request.json)
    else:
        return jsonify({"error": "Method HTTP not allowed"}), 405

    # Restituisci la risposta dal servizio sottostante
    return jsonify(response.json())


@app.route('/api/<string:service>', methods=['GET', 'POST'])
def forward_requests_no_subpath(service):
    return forward_requests(service, None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(get_configs().properties.get('port')))
