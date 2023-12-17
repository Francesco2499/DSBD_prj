from flask import  request, jsonify
from Services.customer_service import CustomerService
from werkzeug.security import check_password_hash, generate_password_hash

class CustomerController:
    def __init__(self):
        self.customer_service = CustomerService()

    def get_all_customers(self):
        customers = self.customer_service.get_all_customers()
        customerList = [customer.__str__() for customer in customers]
        return {"customers" : customerList }

    def get_customer_by_id(self, customer_id):
        customer = self.customer_service.get_customer_by_id(customer_id)
        if customer:
            return customer.__str__()
        else:
            return jsonify(error="Customer not found"), 404

    def create_customer(self, data):
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')

        if not name or not email or not password:
            return jsonify(error="Name, password and email are required"), 400

        new_customer = self.customer_service.create_customer(name, password, email)

        return jsonify(message="Customer created successfully with id: " + str(new_customer.id)), 201
    
    def delete_customer(self, data):
        data = request.json

        # Verifica che ci siano sia l'email che la password nei dati della richiesta
        if 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400

        email = data['email']
        password = data['password']

        # Chiamare il metodo del servizio per eliminare il cliente
        result = self.customer_service.delete_customer(email, password)

        # Restituire una risposta JSON
        return jsonify(result)
    
    def auth(self, data):
        data = request.json
        # Verifica che ci siano sia l'email che la password nei dati della richiesta
        if 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400

        email = data['email']
        password = data['password']

        # Ottieni il cliente dal servizio
        customer = self.customer_service.get_customer_by_email(email)
        if customer:
            return jsonify(self.customer_service.customer_auth(customer, password))
        else:
            # Email o password errati
            return jsonify({"error": "Invalid email or password"}), 401
        
    

customer_controller = CustomerController()

