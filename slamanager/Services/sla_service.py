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
                sla_metric = SlaMetric(metricId=metric_id, desideredValue=sla_value, service=service)
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
            sla_metric_from_db.desideredValue,
            sla_metric_from_db.numberViolations,
            sla_metric_from_db.service,
            sla_metric_from_db.lastCheckTime
        )
    
    def fetch_metrics(self):
        prometheus_url = os.getenv('PROMETHEUS_URL') or config.properties.get('PROMETHEUS_URL')
        prom = PrometheusConnect(url=prometheus_url)
        metrics = self.get_all_sla_metrics()
        for metric in metrics:
            metric_name = self.get_metric_by_id(metric.metric_id).get_name()
            custom_query = f'{metric_name}'
            result = prom.custom_query(query=custom_query)
            print(result)