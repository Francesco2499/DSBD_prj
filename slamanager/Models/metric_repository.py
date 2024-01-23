from MySQLdb import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import get_configs
import os
Base = declarative_base()
config = get_configs()


class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), unique=True)
    slametrics = relationship("SlaMetric", back_populates='metric')


class MetricRepository:
    def __init__(self):
         # Configura la connessione al database MySQL
        DB_HOST = os.getenv('MYSQL_HOST') or config.properties.get('DB_HOST')
        DB_USER = os.getenv('MYSQL_USER') or config.properties.get('DB_USER',)
        DB_PWD = os.getenv('MYSQL_PASSWORD') or config.properties.get('DB_PWD')
        DB_SCHEMA = os.getenv('MYSQL_DATABASE') or config.properties.get('DB_SCHEMA')
        DB_PORT = os.getenv('MYSQL_PORT') or config.properties.get('DB_PORT')

        engine = create_engine(f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_metrics(self):
        return self.session.query(Metric).all()

    def get_metric_by_id(self, metric_id):
        return self.session.query(Metric).filter_by(id=metric_id).first()

    def get_metric_by_name(self, metric_name):
        return self.session.query(Metric).filter_by(name=metric_name).first()

    def create_metric(self, metric):
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
