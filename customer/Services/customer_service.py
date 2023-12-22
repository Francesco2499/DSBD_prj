import requests
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
        if c:
            customer = self.serializeCustomer(c)
            return customer
        return None

    def get_customer_by_email(self, customer_email):
        c = self.customer_repository.get_customer_by_email(customer_email)
        if c:
            customer = self.serializeCustomer(c)
            return customer
        return None

    def create_customer(self, name, password, email):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            customer = Customer(name=name, password=hashed_password, email=email)
            new_customer = self.customer_repository.create_customer(customer)
            return new_customer
        except Exception as e:
            raise e

    def delete_customer(self, email, password):
        customer = self.get_customer_by_email(email)
        result = False
        if (check_password_hash(customer.password, password)):
            result = self.customer_repository.delete_customer(email, customer.password)

        if result:
            return {"message": "Customer deleted successfully"}
        else:
            return {"error": "Failed to delete customer. Invalid email or password."}

    def customer_auth(self, customer, password):
        if check_password_hash(customer.password, password):
            authentication_service_url = 'http://localhost:5002/authenticate'
            payload = {'user_id': customer.customer_id}

            try:
                response = requests.post(authentication_service_url, json=payload)
                response_data = response.json()

                if (response.status_code == 200):
                    return {"message": 'Authentication successful', "token": response_data.get('token')}
                else:
                    return {"message": 'Authentication failed:', "Error": response_data}

            except requests.exceptions.RequestException as e:
                return ('Error during authentication:', e)
        else:
            # password errata
            return {"error": "Invalid name or password"}

    def serializeCustomer(self, customer_from_db):
        return CustomerModel(
            customer_from_db.id,
            customer_from_db.name,
            customer_from_db.password,
            customer_from_db.email
        )
