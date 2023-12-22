import requests
from Models.category_model import CategoryModel
from Models.category_repository import Category, CategoryRepository
from Models.preference_repository import Preference, PreferenceRepository

class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()
        self.preference_repository = PreferenceRepository()

    def get_all_categories(self):
        categoryList = self.category_repository.get_all_categories()
        categories = [self.serializeCategory(c) for c in categoryList]
        return categories

    def get_category_by_id(self, category_id):
        c = self.category_repository.get_category_by_id(category_id)
        if c:
            category = self.serializeCategory(c)
            return category
        return None
    
    def get_category_by_name(self, category_name):
        c = self.category_repository.get_category_by_name(category_name)
        if c:
            category = self.serializeCategory(c)
            return category
        return None
    
    def create_category(self, name):
        category = Category(name=name)
        try:
            new_category = self.category_repository.create_category(category)
            return new_category
        except Exception as e:
            raise e 
    
    def add_preference(self, category_name, user_email):
        try:
            category = self.get_category_by_name(category_name)
            if category:
                categoryId = category.category_id
                preference = Preference(categoryId=categoryId, userEmail=user_email)
                new_preference = self.preference_repository.create_preference(preference)
                return new_preference
            else:
                raise Exception("Errore: Category not found")
        except Exception as e:
            raise e 
        
    def get_emails_by_category(self, category_name):
        emails = self.category_repository.get_emails_by_category(category_name)
        if emails:
            return emails
        else:
            return None
    
    def serializeCategory(self, caregory_from_db):
        return CategoryModel(
            caregory_from_db.id,
            caregory_from_db.name
        )
    
    def verify_token(self, token):
        authentication_service_url = 'http://localhost:5002/verify_token'
        payload = {'token': token.replace('Bearer ', '')}
        print(payload)
        try:
            response = requests.post(authentication_service_url, json=payload)
            response_data = response.json()

            if (response.status_code == 200 and response_data.get('valid')):
                return{"message": 'Authentication successful', 'valid': True}
            else:
                return{"message": 'Authentication failed:', "Error": response_data, 'valid': False}

        except Exception as e:
           raise(e)