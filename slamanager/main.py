from flask import Flask, request, jsonify
from Controllers.sla_controller import SlaController
from config import get_configs

app = Flask(__name__)
sla_controller = SlaController()


@app.route('/metrics/all', methods=['GET'])
def get_all_metrics():
    return sla_controller.get_all_metrics()


@app.route('/metrics/<int:metric_id>', methods=['GET'])
def get_metric_by_id(metric_id):
    return sla_controller.get_metric_by_id(metric_id)


@app.route('/metrics', methods=['GET'])
def get_metric_by_name():
    metric_name = request.args.get('metric-name')
    if metric_name:
        return sla_controller.get_metric_by_name(metric_name)
    else:
        return jsonify("Error: Metric name not provided in the query string"), 400


@app.route('/metrics', methods=['POST'])
def create_metric():
    data = request.json
    return sla_controller.create_metric(data)

@app.route('/add_sla', methods=['POST'])
def add_sla_to_metric():
    data = request.json
    metric_name = data.get('metric_name')
    sla_value = data.get('sla_value')
    service = data.get('service')

    if metric_name and sla_value and service:
        return sla_controller.add_sla_to_metric(metric_name, sla_value, service)
    else:
        return jsonify("Error: Metric name or SLA name or service not provided in the request body"), 400
    
@app.route('/sla_metrics/all', methods=['GET'])
def get_all_sla_metrics():
    return sla_controller.get_all_sla_metrics()

@app.route('/fetch_metrics', methods=['GET'])
def fetch_metrics():
    return sla_controller.fetch_metrics()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(get_configs().properties.get('port')))
