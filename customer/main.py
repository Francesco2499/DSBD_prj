from flask import Flask, request
from Controllers.customer_controller import CustomerController

app = Flask(__name__)
customer_controller = CustomerController()

@app.route('/customers', methods=['GET'])
def get_all_customers():
    return customer_controller.get_all_customers()

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    return customer_controller.get_customer_by_id(customer_id)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    return customer_controller.create_customer(data)

@app.route('/customers/delete', methods=['POST'])
def delete_customer():
    data = request.json
    return customer_controller.delete_customer(data)

@app.route('/customers/auth', methods=['POST'])
def authenticate():
    data = request.json
    return customer_controller.auth(data)

if __name__ == '__main__':
    app.run(debug=True)