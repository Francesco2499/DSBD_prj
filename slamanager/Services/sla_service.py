from flask import jsonify
import pandas as pd
import requests
from Models.slametric_model import SlaMetricModel
from Models.metric_model import MetricModel
from Models.metric_repository import Metric, MetricRepository
from Models.slametric_repository import SlaMetric, SlaRepository
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
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
    
    def get_sla_metric(self, data):
        metric_name = data.get('metric_name')
        service = data.get('service')
        m = self.slametric_repository.get_sla_metric(metric_name, service)
        if m:
            metric = self.serializeSlaMetric(m)
            return metric
        return None
    
    def create_metric(self, name):
        metric = Metric(name=name)
        try:
            new_metric = self.metric_repository.create_metric(metric)
            return new_metric
        except Exception as e:
            raise e 
    
    def add_sla_to_metric(self, data):
        try:
            metric_name = data.get('metric_name')
            service = data.get('service')
            desired_value = data.get('desiredValue')
            max_value = data.get('max')
            min_value = data.get('min')

            metric = self.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric.metric_id
                sla_metric = SlaMetric(metricId=metric_id, name = metric_name, desiredValue=desired_value, service=service, maxValue=max_value, minValue=min_value)
                new_sla = self.slametric_repository.save_metric(sla_metric)
                return new_sla
            else:
                raise Exception("Error: Metric not found")
        except Exception as e:
            raise e 


    def delete_sla(self, data):
        try:
            metric = self.get_sla_metric(data)
            if metric:
                self.slametric_repository.delete_metric(metric)
                return metric
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
            sla_metric_from_db.desiredValue,
            sla_metric_from_db.lastUpdateTime,
            sla_metric_from_db.service,
            sla_metric_from_db.maxValue,
            sla_metric_from_db.minValue
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
                            if metric.min_value < float(value[1])  or float(value[1]) > metric.max_value:
                                nviolation = nviolation + 1                 
                        metric_data =  {
                                'name': metric.name,
                                'desiredValue': metric.desired_value,
                                'lastUpdateSLATime': metric.last_update_time,
                                'numberOfViolation': nviolation,
                                'service': metric.service,
                                'minValue': metric.min_value,
                                'maxValue': metric.max_value
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
                        if metric.min_value < float(value)  or float(value) > metric.max_value:
                            violation = True
                        else:
                            violation = False                      
                        metric_data =  {
                                    'name': metric.name,
                                    'desiredValue': metric.desired_value,
                                    'currentValue': value,
                                    'lastUpdateSLATime': metric.last_update_time,
                                    'violationStatus': violation,
                                    'service': metric.service,
                                    'minValue': metric.min_value,
                                    'maxValue': metric.max_value
                        }
                    response_data.append(metric_data)
            return jsonify(response_data)
        except Exception as e:
            raise e
        
    def get_forecast_violations(self, time_range):
        try:
            prometheus_url = os.getenv('PROMETHEUS_URL') or config.properties.get('PROMETHEUS_URL')
            prom = PrometheusConnect(url=prometheus_url)
            metrics = self.get_all_sla_metrics()
            response_data = []
            for metric in metrics:
                #metric_name = self.get_metric_by_id(metric.metric_id).get_name()
                custom_query = f'{metric.name}{{container_label_com_docker_compose_service="{metric.service}"}}[{time_range}h]'
                result = prom.custom_query(query=custom_query)
                for r in result:
                    service = r.get('metric').get('container_label_com_docker_compose_service')
                    values = r.get('values')
                    if service and values:                                              
                        df = pd.DataFrame(values, columns=['timestamp','value'])
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                        df['value'] = pd.to_numeric(df['value'], errors='coerce')
                        time_series_data = df[['timestamp', 'value']]     
                        pd.set_option('display.float_format', '{:.2f}'.format)
                        time_series_data = time_series_data.set_index('timestamp')

                        print(time_series_data)

                        time_series_data = time_series_data.dropna()  # Rimuovi righe con valori mancanti

                        auto_model = auto_arima(time_series_data['value'], seasonal=False, suppress_warnings=True)
                        best_order = auto_model.order

                        # Stampa i migliori ordini trovati
                        print(f"Best order: {best_order}")
                        
                        future_steps = int(time_range) * 240
                        #Previsioni per i prossimi n periodi
                        forecast, conf_int = auto_model.predict(n_periods=future_steps, return_conf_int=True)
                        nviolations = 0
                        for value in forecast.values:
                            print('{:.2f}'.format(value))
                            if (value > metric.max_value or value < metric.min_value):
                                nviolations += 1
                        prob_violations = nviolations/len(forecast.values)
                        print(prob_violations)

                        response =  {
                                    'name': metric.name,
                                    'desiredValue': metric.desired_value,
                                    'probViolations': prob_violations,                                  
                                    'service': metric.service,
                                    'minValue': metric.min_value,
                                    'maxValue': metric.max_value
                        }
                        response_data.append(response)       
            return jsonify(response_data)
        except Exception as e:
            raise e
        
        