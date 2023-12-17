class CustomerModel:
    def __init__(self, customer_id, name, password, email):
        self.customer_id = customer_id
        self.name = name
        self.password = password
        self.email = email

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password
    
    def get_email(self):
        return self.email

    def set_name(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password    

    def set_email(self, email):
        self.email = email

    def __str__(self):
        return {
            "CustomerID": self.customer_id, 
            "Name": self.name, 
            "Email": self.email
        }
