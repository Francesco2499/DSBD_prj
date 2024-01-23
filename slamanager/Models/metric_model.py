class MetricModel:
    def __init__(self, metric_id, name):
        self.metric_id = metric_id
        self.name = name

    def get_metric_id(self):
        return self.metric_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return {
            "MetricID": self.metric_id, 
            "Name": self.name
        }
