from typing import Any 
import shutil
import tempfile
#import asyncio
import time

import flask
#import flask_socketio
from flask_sse import sse

from . import config_gen_bp

from .models import ConfigParam, Params, generate_feature_models




@config_gen_bp.route('/')
def index():
    params = get_parameters_from_request(None)
    return flask.render_template('config_gen/index.html', params=params)


def generate():
    x = 0
    while x <= 100:
        yield "event: progress_bar\ndata:" + str(x) + "\n\n"
        x = x + 10
        time.sleep(0.5)


def stream_template(template_name, **context):
    flask.current_app.update_template_context(context)
    t = flask.current_app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@config_gen_bp.route('/progress')
def progress():
    if flask.request.method == 'GET':    
        #data = generate_feature_models(params)
        #return flask.current_app.response_class(stream_template('config_gen/index.html', data=data), mimetype='text/event-stream')
        return flask.Response(generate(), mimetype='text/event-stream')
        #return flask.Response(generate_feature_models(params), mimetype='text/event-stream')


@config_gen_bp.route('/', methods=['GET', 'POST'])
def fms_gen():
    request = flask.request
    if request.method == 'GET' or request.method == 'POST':
        params = get_parameters_from_request(None)
        return flask.render_template('config_gen/index.html', params=params)
    if request.method == 'POST':
        params = get_parameters_from_request(request)
        return flask.Response(generate(), mimetype='text/event-stream')
        # Generate random feature models
        with tempfile.TemporaryDirectory() as temp_dir:
            params[Params.SERIALIZATION_TEMPORAL_DIR.name] = Params.SERIALIZATION_TEMPORAL_DIR.value.to_dict()
            params[Params.SERIALIZATION_TEMPORAL_DIR.name]['value'] = temp_dir

            return flask.Response(generate_feature_models(params), mimetype='text/event-stream')
            # Prepare files for download
            temp_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
            temp_zipfile = shutil.make_archive(temp_filepath, 'zip', temp_dir)
            zip_filename = f"{params[Params.MODEL_NAME_PREFIX.name]['value']}{params[Params.NUM_MODELS.name]['value']}.zip"
            response = flask.make_response(flask.send_file(path_or_file=temp_zipfile, 
                                                            as_attachment=True, 
                                                            download_name=zip_filename))
        return response


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
    
