from flask import Flask, request
from Controllers import subscriber_controller

import sys

sys.path.append("Controllers/")

app = Flask(__name__)


@app.route('/subscribe', methods=['GET'])
def subscribe():
    result = subscriber_controller.subscribe_category()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)
