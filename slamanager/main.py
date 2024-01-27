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
    service = data.get('service')

    if metric_name and service:
        return sla_controller.add_sla_to_metric(data)
    else:
        return jsonify("Error: Metric name or service not provided in the request body"), 400
    
@app.route('/delete_sla', methods=['POST'])
def delete_sla():
    data = request.json
    metric_name = data.get('metric_name')
    service = data.get('service')

    if metric_name and service:
        return sla_controller.delete_sla(data)
    else:
        return jsonify("Error: Metric name or service not provided in the request body"), 400
    
@app.route('/sla_metrics/all', methods=['GET'])
def get_all_sla_metrics():
    return sla_controller.get_all_sla_metrics()

@app.route('/violations', methods=['GET'])
def get_violations():
    time_range = request.args.get('time-range')
    return sla_controller.get_violations(time_range)

@app.route('/check_sla', methods=['GET'])
def check_sla():
    return sla_controller.check_sla()

@app.route('/forecast_violations', methods=['GET'])
def get_forecast_violations():
    time_range = request.args.get('time-range')
    return sla_controller.get_forecast_violations(time_range)

if __name__ == '__main__':
    metric_names = ['container_memory_usage_bytes', 'container_start_time_seconds', 'container_network_transmit_errors_total']
    existing_metrics = sla_controller.get_all_metrics().get('metrics', [])
    existing_metric_names = [metric.get('Name') for metric in existing_metrics]

    for metric_name in metric_names:
        if metric_name not in existing_metric_names:
            data = {
                "name": metric_name
            }
            sla_controller.create_metric(data)
        
            create_metric(metric_name)
    app.run(host='0.0.0.0', debug=True, port=int(get_configs().properties.get('port')))
