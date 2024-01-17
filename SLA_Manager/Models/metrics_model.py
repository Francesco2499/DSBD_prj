class SLAMetricModel:
    def __init__(self, metric_id, name, desired_value, current_value, violations, last_check_time):
        self.metric_id = metric_id
        self.name = name
        self.desired_value = desired_value
        self.current_value = current_value
        self.violations = violations
        self.last_check_time = last_check_time

    def get_id(self):
        return self.metric_id

    def get_name(self):
        return self.name

    def get_desired_value(self):
        return self.desired_value

    def get_current_value(self):
        return self.current_value

    def get_violations(self):
        return self.violations

    def get_last_check_time(self):
        return self.last_check_time

    def set_name(self, name):
        self.name = name

    def set_desired_value(self, desired_value):
        self.desired_value = desired_value

    def set_current_value(self, current_value):
        self.current_value = current_value

    def set_violations(self, violations):
        self.violations = violations

    def set_last_check_time(self, last_check_time):
        self.last_check_time = last_check_time

    def __str__(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "DesiredValue": self.desired_value,
            "CurrentValue": self.current_value,
            "Violations": self.violations,
            "LastCheckTime": self.last_check_time
        }