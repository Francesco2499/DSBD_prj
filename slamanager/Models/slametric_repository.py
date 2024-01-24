from MySQLdb import IntegrityError
# from mysqlx import Session
from sqlalchemy import BOOLEAN,  ForeignKey, UniqueConstraint, create_engine, Column, Integer, String, Float, Double, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from Models.metric_repository import Base
from config import get_configs
from datetime import datetime, timezone

import os

config = get_configs()


class SlaMetric(Base):
    __tablename__ = 'slametrics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    metricId = Column(Integer, ForeignKey('metrics.id'))
    name = Column(String(256))
    desideredValue = Column(Double, nullable=False)
    lastUpdateTime = Column(DateTime, default=datetime.now(timezone.utc))
    service = Column(String(256))
    metric = relationship("Metric", back_populates='slametrics')

__table_args__ = (
        UniqueConstraint('name', 'service', name='uq_name_service'),
    )


class SlaRepository:
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
            existing_metric = self.session.query(SlaMetric).filter_by(name=metric.name, service=metric.service).first()

            if existing_metric:
                # Se la metrica esiste già, aggiorna i suoi valori
                existing_metric.desideredValue = metric.desideredValue
                existing_metric.lastUpdateTime = datetime.now(timezone.utc)
            else:
                # Se la metrica non esiste, esegui una nuova insert
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
        
        if existing_metric:
            return existing_metric
        else:    
            return metric


    def get_all_sla_metrics(self):
        return self.session.query(SlaMetric).all()

    def get_sla_metric_by_id(self, metric_id):
        return self.session.query(SlaMetric).filter_by(metricId=metric_id).first()

    def get_sla_metric_by_name(self, name):
        return self.session.query(SlaMetric).filter_by(name=name).first()

    def delete_metric(self, metric_id):
        metric_to_delete = self.session.query(SlaMetric).filter_by(metricId=metric_id).first()
        if metric_to_delete:
            self.session.delete(metric_to_delete)
            self.session.commit()
            return True
        else:
            return False
