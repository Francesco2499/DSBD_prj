from flask import Flask, request
from Controllers import subscriber_controller

import sys

sys.path.append("Controllers/")

app = Flask(__name__)


@app.route('/subscribe', methods=['GET'])
def subscribe():
    category = request.args.get('category', 'general')  # Se non specificata, default a 'general'
    result = subscriber_controller.subscribe_category(category)
    return result


if __name__ == '__main__':
    app.run(debug=True, port=5000)
