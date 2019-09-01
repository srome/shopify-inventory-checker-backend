from flask import Flask
from flask_cors import CORS
from inventory import Handler
from json import dumps as to_json

application = Flask(__name__)
CORS(application)

@application.route("/")
def index():
    return to_json(Handler.get_content())

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=3000)