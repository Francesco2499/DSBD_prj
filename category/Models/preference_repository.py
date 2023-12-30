from MySQLdb import IntegrityError
from sqlalchemy import ForeignKey, UniqueConstraint, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from Models.category_repository import Base
from config import get_configs
import os

config = get_configs()

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryId = Column(Integer, ForeignKey('categories.id'))
    userEmail = Column(String(50))
    category = relationship("Category", back_populates='preferences')

    __table_args__ = (
        UniqueConstraint('categoryId', 'userEmail', name='uq_category_user_email'),
    )

class PreferenceRepository:
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