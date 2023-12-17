from MySQLdb import IntegrityError
from mysqlx import Session
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(String(50))
    email = Column(String(50))

class CustomerRepository:
    def __init__(self):
        # Configura la connessione al database MySQL
        engine = create_engine('mysql://root:root@localhost/dsbd_customer', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_new_session(self):
        new_session = Session()
        return new_session
    
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
