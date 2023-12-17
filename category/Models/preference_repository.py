from MySQLdb import IntegrityError
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from Models.category_repository import Base
#Base = declarative_base()

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryId = Column(Integer, ForeignKey('categories.id'))
    userEmail = Column(String(50))
    category = relationship("Category")

class PreferenceRepository:
    def __init__(self):
        # Configura la connessione al database MySQL
        engine = create_engine('mysql://root:root@localhost/dsbd_category', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_preferences(self):
        return self.session.query(Preference).all()

    def get_preference_by_id(self, preference_id):
        return self.session.query(Preference).filter_by(id=preference_id).first()
    
    def create_preference(self, preference):
        try:
            self.session.add(preference)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            self.session.close()
            raise e
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise e  
        return preference