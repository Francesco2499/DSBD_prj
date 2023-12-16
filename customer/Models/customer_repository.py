from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String(50))
    email = Column(String(50))

class CustomerRepository:
    def __init__(self):
        # Configura la connessione al database MySQL
        engine = create_engine('mysql://root:root@localhost/dsbd', echo=True)
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
        self.session.add(customer)
        self.session.commit()
        return customer
    
    def delete_customer(self, email, password):
        customer_to_delete = self.session.query(Customer).filter_by(email=email, password=password).first()

        if customer_to_delete:
            self.session.delete(customer_to_delete)
            self.session.commit()
            return True
        else:
            return False
