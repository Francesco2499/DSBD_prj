class SlaMetricModel:
    def __init__(self, metric_id, name, desired_value, last_update_time, service):
        self.metric_id = metric_id
        self.name = name
        self.desired_value = desired_value
        self.last_update_time = last_update_time
        self.service = service

    def get_id(self):
        return self.id
    
    def get_metric_id(self):
        return self.metric_id
    
    def get_name(self):
        return self.name

    def get_desired_value(self):
        return self.desired_value

    def get_last_update_time(self):
        return self.last_update_time
    
    def get_service(self):
        return self.service

    def set_name(self, name):
        self.name = name
    
    def set_desired_value(self, desired_value):
        self.desired_value = desired_value

    def set_last_update_time(self, last_update_time):
        self.last_update_time = last_update_time
    
    def set_service(self, service):
        self.service = service

    def __str__(self):
        return {
            "MetricId": self.metric_id,
            "Name": self.name,
            "DesiredValue": self.desired_value,
            "LastUpdateTime": self.last_update_time,
            "Service": self.service
        }