from typing import Any 

import flask

from . import config_gen_bp

from .models import Params


@config_gen_bp.route('/')
def index():
    params = get_parameters_from_request(None)
    return flask.render_template('config_gen/index.html', params=params)


@config_gen_bp.route('/', methods=['POST'])
def fms_gen():
    request = flask.request
    if request.method == 'POST':
        params = get_parameters_from_request(request)
        print(f'#Models: {params['num_models']}')
        return flask.render_template('config_gen/index.html', params=params) 
    else:
        flask.render_template('config_gen/index.html') 


def get_parameters_from_request(request: flask.Request) -> dict[str, Any]:
    params = dict()
    params['num_models'] = request.form['num_models'] if request else 1
    return params