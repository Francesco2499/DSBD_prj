from Models.customer_model import CustomerModel
from Models.customer_repository import Customer, CustomerRepository
from werkzeug.security import generate_password_hash, check_password_hash

class CustomerService:
    def __init__(self):
        self.customer_repository = CustomerRepository()

    def get_all_customers(self):
        customerList = self.customer_repository.get_all_customers()
        customers = [self.serializeCustomer(c) for c in customerList]
        return customers

    def get_customer_by_id(self, customer_id):
        c = self.customer_repository.get_customer_by_id(customer_id)
        customer = self.serializeCustomer(c)
        return customer
    
    def get_customer_by_email(self, customer_email):
        c = self.customer_repository.get_customer_by_email(customer_email)
        customer = self.serializeCustomer(c)
        return customer

    def create_customer(self, name, password, email):
        hashed_password = generate_password_hash(password, method='sha256')
        new_customer = Customer(name=name, password=hashed_password, email=email)
        return self.customer_repository.create_customer(new_customer)
    
    def delete_customer(self, email, password):
        customer = self.get_customer_by_email(email)
        result = False
        if(check_password_hash(customer.password, password)):
            result = self.customer_repository.delete_customer(email, customer.password)

        if result:
            return {"message": "Customer deleted successfully"}
        else:
            return {"error": "Failed to delete customer. Invalid email or password."}
        
    def customer_auth(self, customer, password):
        result = False
        if(check_password_hash(customer.password, password)):
            return {"message": "Authentication successful"}
        else:
            #password errata
            return {"error": "Invalid name or password"}
        
    
    def serializeCustomer(self, customer_from_db):
        return CustomerModel(
            customer_from_db.id,
            customer_from_db.name,
            customer_from_db.password,
            customer_from_db.email
        )
        