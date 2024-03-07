import os

import dotenv

from config import create_app

from blueprints.config_gen import config_gen_bp


# Load configurables (environment) variables from a configuration file
dotenv.load_dotenv()

# Create the App
flask_app = create_app()
celery_app = flask_app.extensions['celery']

# Configure Flask app
flask_app.template_folder = 'templates'
flask_app.static_folder = 'static'
flask_app.static_url_path = '/static'
#app.config['GENERATION_FOLDER'] = os.getenv('GENERATION_FOLDER')
#flask_app.config["REDIS_URL"] = "redis://localhost"
#app.register_blueprint(sse, url_prefix='/progress')

# Register blueprints
flask_app.register_blueprint(config_gen_bp, url_prefix='/')


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)

    flask_app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
