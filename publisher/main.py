from flask import Flask
from Controllers import publisher_controller
from apscheduler.schedulers.background import BackgroundScheduler
from configs import config

import sys
import os

sys.path.append("Controllers/")
sys.path.append("configs/")

app = Flask(__name__)

is_publisher_active = False
scheduler = None

configs = config.get_configs()


@app.route('/publish_news', methods=['GET'])
def publish_news_async():
    result = publish_news()
    return result


def publish_news():
    result = publisher_controller.get_news_by_category()  # Chiamata effettiva alla funzione
    print(result)
    return result


def start_publisher():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(publish_news, 'interval', hours=8)
    scheduler.start()


if __name__ == "__main__":
    if os.environ.get('IS_TEST') or configs.properties.get('IS_TEST'):
        app.run(host='0.0.0.0', debug=True, port=5001)
    else:
        start_publisher()