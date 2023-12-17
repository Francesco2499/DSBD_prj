class CategoryModel:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    def get_category_id(self):
        return self.category_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return {
            "CategoryID": self.category_id, 
            "Name": self.name
        }
