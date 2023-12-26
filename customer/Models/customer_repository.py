from MySQLdb import IntegrityError
#from mysqlx import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_configs
import os

Base = declarative_base()
config = get_configs()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(String(256))
    email = Column(String(50), unique=True)


class CustomerRepository:
    def __init__(self):
        # Configura la connessione al database MySQL
        DB_HOST = os.getenv('MYSQL_HOST') or config.properties.get('DB_HOST')
        DB_USER = os.getenv('MYSQL_USER') or config.properties.get('DB_USER',)
        DB_PWD = os.getenv('MYSQL_PASSWORD') or config.properties.get('DB_PWD')
        DB_SCHEMA = os.getenv('MYSQL_DATABASE') or config.properties.get('DB_SCHEMA')

        engine = create_engine(f'mysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_SCHEMA}', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_customers(self):
        return self.session.query(Customer).all()

    def get_customer_by_id(self, customer_id):
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def get_customer_by_email(self, customer_email):
        return self.session.query(Customer).filter_by(email=customer_email).first()

    def create_customer(self, customer):
        try:
            self.session.add(customer)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            self.session.close()
            raise e
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise e
        return customer

    def delete_customer(self, email, password):
        customer_to_delete = self.session.query(Customer).filter_by(email=email, password=password).first()
        if customer_to_delete:
            self.session.delete(customer_to_delete)
            self.session.commit()
            return True
        else:
            return False
