from flask import Flask
from Controllers import publisher_controller

import sys

sys.path.append("Controllers/")

app = Flask(__name__)


@app.route('/publish_news', methods=['POST'])
def publish_news():
    return publisher_controller.get_news_by_category()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
