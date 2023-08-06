import os
from scapinspector import api
from scapinspector.api_static import api as api_static

from flask import Flask

app = Flask(__name__, static_url_path='')
app.register_blueprint(api)
app.register_blueprint(api_static)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
