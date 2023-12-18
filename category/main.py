from flask import Flask, request, jsonify
from Controllers.category_controller import CategoryController

app = Flask(__name__)
category_controller = CategoryController()

@app.route('/categories/all', methods=['GET'])
def get_all_categories():
    return category_controller.get_all_categories()

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    return category_controller.get_category_by_id(category_id)

@app.route('/categories', methods=['GET'])
def get_category_by_name():
    category_name = request.args.get('category-name')
    if category_name:
        return category_controller.get_category_by_name(category_name)
    else:
        return jsonify("Error: Category name not provided in the query string"), 400

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    return category_controller.create_category(data)

@app.route('/categories/add-preference', methods=['POST'])
def add_preference():
    token = request.headers.get('Authorization')

    if not token or token == '':
        return jsonify(error="Authorization Token is Required"), 401
    else:
        verify_token = category_controller.verify_token(token)
        valid = verify_token.get('valid')
        if(valid):
            data = request.json
            return category_controller.add_preference(data)
        else:
            return verify_token, 401
        
@app.route('/categories/preferences', methods=['GET'])
def get_emails_by_category():
    category_name = request.args.get('category-name')
    if category_name:
        return category_controller.get_emails_by_category(category_name)
    else:
        return jsonify("Error: Category name not provided in the query string"), 400


if __name__ == '__main__':
    app.run(debug=True, port=8082)