from MySQLdb import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    preferences = relationship("Preference", back_populates='category')


class CategoryRepository:
    def __init__(self):
        # Configura la connessione al database MySQL
        engine = create_engine('mysql://root:root@localhost/dsbd_category', echo=True)
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
