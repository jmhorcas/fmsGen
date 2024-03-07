import os
import threading

import dotenv

import flask
from flask_sse import sse

from flask_socketio import SocketIO

from blueprints.config_gen import config_gen_bp


# Load configurables (environment) variables from a configuration file
dotenv.load_dotenv()

# Create the App
app = flask.Flask(__name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/static')
#app.config['GENERATION_FOLDER'] = os.getenv('GENERATION_FOLDER')
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/progress')

# Register blueprints
app.register_blueprint(config_gen_bp, url_prefix='/')


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)

    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, threaded=True, debug=ENVIRONMENT_DEBUG)
