from flask import Flask
from Controllers import subscriber_controller

import sys

sys.path.append("Controllers/")

app = Flask(__name__)


def subscribe():
    result = subscriber_controller.subscribe_category()
    return result


if __name__ == "__main__":
    subscribe()



