from flask import request, jsonify
from Services.sla_service import SlaService


class SlaController:
    def __init__(self):
        self.sla_service = SlaService()

    def get_all_metrics(self):
        metrics = self.sla_service.get_all_metrics()
        metricList = [metric.__str__() for metric in metrics]
        return {"metrics": metricList}

    def get_metric_by_id(self, metric_id):
        metric = self.sla_service.get_metric_by_id(metric_id)
        if metric:
            return metric.__str__()
        else:
            return jsonify(error="Metric not found"), 404

    def get_metric_by_name(self, metric_name):
        metric = self.sla_service.get_metric_by_name(metric_name)
        if metric:
            return metric.__str__()
        else:
            return jsonify(error="Metric not found"), 404

    def create_metric(self, data):
        name = data.get('name')

        if not name:
            return jsonify(error="Name are required"), 400
        try:
            new_metric = self.sla_service.create_metric(name)
            return jsonify(message="Metric created successfully with id: " + str(new_metric.id)), 201
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 400
        
    def add_sla_to_metric(self, metric_name, sla_value, service):
        if not metric_name or not sla_value:
            return jsonify(error="Metric Name ,SLA Value and Service are required"), 400
        try:
            new_sla = self.sla_service.add_sla_to_metric(metric_name, sla_value, service)
            return jsonify(message="SLA created successfully with id: " + str(new_sla.id)), 201
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 400
        
    def get_all_sla_metrics(self):
        sla_metrics = self.sla_service.get_all_sla_metrics()
        sla_metricList = [sla_metric.__str__() for sla_metric in sla_metrics]
        return {"sla_metrics": sla_metricList}
    
    def get_violations(self, time_range):
        try:
            response = self.sla_service.get_violations(time_range)
            return response, 200
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 500
        
    def check_sla(self):
        try:
            response = self.sla_service.check_sla()
            return response, 200
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 500
        
        
