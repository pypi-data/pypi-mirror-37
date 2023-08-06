import os
from scapinspector.api import api
from scapinspector.api_static import api as api_static
from scapinspector.main import load_config
from flask import Flask

app = Flask(__name__, static_url_path='')
app.register_blueprint(api)
app.register_blueprint(api_static)


if __name__ == "__main__":
    load_config()
    app.run(host="0.0.0.0")
