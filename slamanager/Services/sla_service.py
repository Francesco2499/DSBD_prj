from flask import jsonify
import requests
from Models.slametric_model import SlaMetricModel
from Models.metric_model import MetricModel
from Models.metric_repository import Metric, MetricRepository
from Models.slametric_repository import SlaMetric, SlaRepository
from prometheus_api_client import PrometheusConnect
from config import get_configs
import os

config = get_configs()


class SlaService:
    def __init__(self):
        self.metric_repository = MetricRepository()
        self.slametric_repository = SlaRepository()

    def get_all_metrics(self):
        metricList = self.metric_repository.get_all_metrics()
        metrics = [self.serializeMetric(m) for m in metricList]
        return metrics

    def get_metric_by_id(self, metric_id):
        m = self.metric_repository.get_metric_by_id(metric_id)
        if m:
            metric = self.serializeMetric(m)
            return metric
        return None
    
    def get_metric_by_name(self, metric_name):
        m = self.metric_repository.get_metric_by_name(metric_name)
        if m:
            metric = self.serializeMetric(m)
            return metric
        return None
    
    def create_metric(self, name):
        metric = Metric(name=name)
        try:
            new_metric = self.metric_repository.create_metric(metric)
            return new_metric
        except Exception as e:
            raise e 
    
    def add_sla_to_metric(self, metric_name, sla_value, service):
        try:
            metric = self.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric.metric_id
                sla_metric = SlaMetric(metricId=metric_id, name = metric_name, desideredValue=sla_value, service=service)
                new_sla = self.slametric_repository.save_metric(sla_metric)
                return new_sla
            else:
                raise Exception("Error: Metric not found")
        except Exception as e:
            raise e 

    def get_all_sla_metrics(self):
        sla_metricList = self.slametric_repository.get_all_sla_metrics()
        sla_metrics = [self.serializeSlaMetric(sm) for sm in sla_metricList]
        return sla_metrics
    
    def serializeMetric(self, metric_from_db):
        return MetricModel(
            metric_from_db.id,
            metric_from_db.name
        )
    
    def serializeSlaMetric(self, sla_metric_from_db):
        return SlaMetricModel(
            sla_metric_from_db.metricId,
            sla_metric_from_db.name,
            sla_metric_from_db.desideredValue,
            sla_metric_from_db.lastUpdateTime,
            sla_metric_from_db.service
        )
    
    def get_violations(self, time_range):
        try:
            prometheus_url = os.getenv('PROMETHEUS_URL') or config.properties.get('PROMETHEUS_URL')
            prom = PrometheusConnect(url=prometheus_url)
            metrics = self.get_all_sla_metrics()
            response_data = []
            for metric in metrics:
                #metric_name = self.get_metric_by_id(metric.metric_id).get_name()
                custom_query = f'{metric.name}{{container_label_com_docker_compose_service="{metric.service}"}}[{time_range}]'
                result = prom.custom_query(query=custom_query)
                print(result)
                for r in result:
                    service = r.get('metric').get('container_label_com_docker_compose_service')
                    values = r.get('values')
                    if service and values:
                        nviolation = 0
                        for value in values:
                            if metric.desired_value <= float(value[1]):
                                nviolation = nviolation + 1                 
                        metric_data =  {
                                'name': metric.name,
                                'desideredValue': metric.desired_value,
                                'lastUpdateSLATime': metric.last_update_time,
                                'numberOfViolation': nviolation,
                                'service': metric.service
                        }
                        response_data.append(metric_data)
            return jsonify(response_data)
        except Exception as e:
            raise e
        
    def check_sla(self):
        try:
            prometheus_url = os.getenv('PROMETHEUS_URL') or config.properties.get('PROMETHEUS_URL')
            prom = PrometheusConnect(url=prometheus_url)
            metrics = self.get_all_sla_metrics()
            response_data = []
            for metric in metrics:
                custom_query = f'{metric.name}{{container_label_com_docker_compose_service="{metric.service}"}}'
                result = prom.custom_query(query=custom_query)
                print(result)
                for r in result:
                    service = r.get('metric').get('container_label_com_docker_compose_service')
                    value = float(r.get('value')[1])
                    if service and value:
                        if metric.desired_value <= float(value):
                            violation = True
                        else:
                            violation = False                      
                        metric_data =  {
                                    'name': metric.name,
                                    'desideredValue': metric.desired_value,
                                    'currentValue': value,
                                    'lastUpdateSLATime': metric.last_update_time,
                                    'violationStatus': violation,
                                    'service': metric.service
                        }
                    response_data.append(metric_data)
            return jsonify(response_data)
        except Exception as e:
            raise e