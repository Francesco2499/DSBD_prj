from MySQLdb import IntegrityError
# from mysqlx import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_configs
from datetime import datetime, timezone

import os

Base = declarative_base()
config = get_configs()


class SLAMetric(Base):
    __tablename__ = 'sla_metrics'
    metrics_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    desired_value = Column(Float, nullable=False)
    number_violations = Column(Integer, default=0)
    last_check_time = Column(DateTime, default=datetime.now(timezone.utc))


class SLAMetric:
    def __init__(self):
        # Configura la connessione al database MySQL
        DB_HOST = os.getenv('MYSQL_HOST') or config.properties.get('DB_HOST')
        DB_USER = os.getenv('MYSQL_USER') or config.properties.get('DB_USER', )
        DB_PWD = os.getenv('MYSQL_PASSWORD') or config.properties.get('DB_PWD')
        DB_SCHEMA = os.getenv('MYSQL_DATABASE') or config.properties.get('DB_SCHEMA')

        engine = create_engine(f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_SCHEMA}', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def save_metric(self, metric):
        try:
            self.session.add(metric)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            self.session.close()
            raise e
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise e
        return metric

    def check_metric_status(self, metric_id, current_value):
        metric = self.session.query(SLAMetric).filter_by(metric_id=metric_id)
        metric.violations = current_value > metric.desired_value
        return metric.violations

    def get_violations_in_time_range(self, metric_id, start_time, end_time):
        result = (self.session.query(SLAMetric).filter_by(metric_id=metric_id, violations=True)
                  .filter(and_(
                    SLAMetric.last_check_time >= start_time,
                    SLAMetric.last_check_time <= end_time,
                  ))
                  .count())
        return result

    def get_probability_of_violation(self, next_interval_minutes):
        # Logica per calcolare la probabilità di violazione nel prossimo intervallo di tempo
        current_violation_rate = self.violations / (
                (datetime.datetime.utcnow() - self.last_check_time).total_seconds() / 60)
        return current_violation_rate * next_interval_minutes

    def get_all_metrics(self):
        return self.session.query(SLAMetric).all()

    def get_metrics_by_id(self, metrics_id):
        return self.session.query(SLAMetric).filter_by(metrics_id=metrics_id).first()

    def get_metric_by_name(self, name):
        return self.session.query(SLAMetric).filter_by(name=name).first()

    def delete_metrics(self, metrics_id):
        metrics_to_delete = self.session.query(SLAMetric).filter_by(metrics_id=metrics_id).first()
        if metrics_to_delete:
            self.session.delete(metrics_to_delete)
            self.session.commit()
            return True
        else:
            return False
