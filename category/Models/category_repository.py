from MySQLdb import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import get_configs
import os
Base = declarative_base()
config = get_configs()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    preferences = relationship("Preference", back_populates='category')


class CategoryRepository:
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

    def get_all_categories(self):
        return self.session.query(Category).all()

    def get_category_by_id(self, category_id):
        return self.session.query(Category).filter_by(id=category_id).first()

    def get_category_by_name(self, category_name):
        return self.session.query(Category).filter_by(name=category_name).first()

    def get_emails_by_category(self, category_name):
        category = self.get_category_by_name(category_name)
        print(category)
        if category:
            emails = [preference.userEmail for preference in category.preferences]
            return emails
        return None

    def create_category(self, category):
        try:
            self.session.add(category)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            self.session.close()
            raise e
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise e
        return category
