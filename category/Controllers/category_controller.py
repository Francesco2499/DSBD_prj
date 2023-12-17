from flask import  request, jsonify
from Services.category_service import CategoryService

class CategoryController:
    def __init__(self):
        self.category_service = CategoryService()

    def get_all_categories(self):
        categories = self.category_service.get_all_categories()
        categoryList = [category.__str__() for category in categories]
        return {"categories" : categoryList }

    def get_category_by_id(self, category_id):
        category = self.category_service.get_category_by_id(category_id)
        if category:
            return category.__str__()
        else:
            return jsonify(error="Category not found"), 404
    
    def get_category_by_name(self, category_name):
        category = self.category_service.get_category_by_name(category_name)
        if category:
            return category.__str__()
        else:
            return jsonify(error="Category not found"), 404
        
    def create_category(self, data):
        name = data.get('name')

        if not name:
            return jsonify(error="Name are required"), 400
        try:
            new_category = self.category_service.create_category(name)
            return jsonify(message="Category created successfully with id: " + str(new_category.id)), 201
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 400
        
    def add_preference(self, data):
        category_name = data.get('categoryName')
        user_email = data.get('userEmail')

        if not category_name or not user_email:
            return jsonify(error="Category Name and User Email are required"), 400
        try:
            new_preference = self.category_service.add_preference(category_name, user_email)
            return jsonify(message="Preference created successfully with id: " + str(new_preference.id)), 201
        except Exception as e:
            print(e)
            return jsonify("Error: " + e.args[0].__str__()), 400
        
    def verify_token(self,token):
        try:
            return self.category_service.verify_token(token)
        except Exception as e:
            return {"message": 'Authentication failed:', "Error": e.args[0].__str__(), 'valid': False}  

category_controller = CategoryController()