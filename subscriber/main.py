from flask import Flask, request
from Controllers import subscriber_controller

import sys

sys.path.append("configs/")

app = Flask(__name__)


@app.route('/subscribe', methods=['GET'])
def subscribe():
    category = request.args.get('category', 'general')  # Se non specificata, default a 'news'
    subscriber_controller.subscribe_category(category)


if __name__ == '__main__':
    app.run(port=5000)
