from typing import Any 
import shutil
import tempfile
import asyncio

import flask
import flask_socketio

from . import config_gen_bp

from .models import ConfigParam, Params, generate_feature_models




@config_gen_bp.route('/')
def index():
    params = get_parameters_from_request(None)
    return flask.render_template('config_gen/index.html', params=params)


@config_gen_bp.route('/', methods=['POST'])
def fms_gen():
    request = flask.request
    if request.method == 'POST':
        params = get_parameters_from_request(request)

        # Generate random feature models
        with tempfile.TemporaryDirectory() as temp_dir:
            params[Params.SERIALIZATION_TEMPORAL_DIR.name] = Params.SERIALIZATION_TEMPORAL_DIR.value.to_dict()
            params[Params.SERIALIZATION_TEMPORAL_DIR.name]['value'] = temp_dir

            generate_feature_models(params)
        
            # Prepare files for download
            temp_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
            temp_zipfile = shutil.make_archive(temp_filepath, 'zip', temp_dir)
            zip_filename = f"{params[Params.MODEL_NAME_PREFIX.name]['value']}{params[Params.NUM_MODELS.name]['value']}.zip"
            response = flask.make_response(flask.send_file(path_or_file=temp_zipfile, 
                                                            as_attachment=True, 
                                                            download_name=zip_filename))
        return response
    else:
        flask.render_template('config_gen/index.html') 


def get_parameters_from_request(request: flask.Request) -> dict[dict[str, Any]]:
    if not request:
        config_params = {param.name: param.value.to_dict() for param in Params}
    else:    
        config_params: dict[dict[str, Any]] = dict()
        for param in Params:
            value = request.form.get(param.name, None) if request else None
            param.value.value = value
            config_params[param.name] = param.value.to_dict()
    return config_params
    
