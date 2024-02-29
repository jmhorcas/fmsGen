from typing import Any 
import shutil
import tempfile

import flask

from . import config_gen_bp

from .models import generate_feature_models


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

        # Generate random feature models
        with tempfile.TemporaryDirectory() as temp_dir:
            generate_feature_models(params['num_models'], temp_dir)
        
            # Prepare files for download
            temp_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
            temp_zipfile = shutil.make_archive(temp_filepath, 'zip', temp_dir)
            response = flask.make_response(flask.send_file(path_or_file=temp_zipfile, 
                                                            as_attachment=True, 
                                                            download_name='models.zip'))
        return response
    else:
        flask.render_template('config_gen/index.html') 


def get_parameters_from_request(request: flask.Request) -> dict[str, Any]:
    params = dict()
    params['num_models'] = int(request.form['num_models']) if request else 1
    return params