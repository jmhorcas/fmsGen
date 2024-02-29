from flask import Blueprint


# Create the blueprint instance
config_gen_bp = Blueprint('config_gen',
                          __name__,
                          template_folder='templates',
                          static_folder='static',
                          static_url_path='/config_gen/static')


# Import the routes module
from . import routes
