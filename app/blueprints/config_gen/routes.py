from typing import Any 

import flask
from celery.result import AsyncResult

from . import config_gen_bp

from .models import Params, generate_feature_models


@config_gen_bp.route('/')
def index():
    params = get_parameters_from_request(None)
    return flask.render_template('config_gen/index.html', params=params)


@config_gen_bp.route("/update_progress/<task_id>", methods=['GET'])
def update_progress(task_id) -> dict[str, object]:
    task = AsyncResult(task_id)
    if task.ready():
        # Task has completed
        if task.successful():
            data = 'data: 100\n\n'
            return flask.Response(data, mimetype="text/event-stream")
        else:
            # Task completed with an error
            #flask.flash(f"The generation task has completed with an error.", category='error')
            return flask.redirect(flask.url_for('config_gen.index'))
    elif task.status == 'PENDING':
        data = 'data: 0\n\n'
        return flask.Response(data, mimetype="text/event-stream")
    elif task.status == 'PROGRESS':
        percentage_completed = int((task.info['current'] / task.info['total']) * 100)
        data = f'data: {percentage_completed}\n\n'
        return flask.Response(data, mimetype="text/event-stream")

@config_gen_bp.route("/get_result/<task_id>", methods=['GET'])
def task_result(task_id) -> dict[str, object]:
    task = AsyncResult(task_id)
    if task.ready():
        # Task has completed
        if task.successful():
            params = task.result
            temp_zipfile = params[Params.ZIP_FILE.name]['value']
            zip_filename = params[Params.ZIP_FILENAME.name]['value']
            response = flask.make_response(flask.send_file(path_or_file=temp_zipfile, 
                                                           as_attachment=True, 
                                                           download_name=zip_filename))
            return response
        else:
            # Task completed with an error
            #flask.flash(f"The generation task has completed with an error.", category='error')
            return flask.redirect(flask.url_for('config_gen.index'))
    else:
        # Task completed with an error
        #flask.flash(f"Error in the generation task.", category='error')
        return flask.redirect(flask.url_for('config_gen.index'))
    

@config_gen_bp.route('/', methods=['POST'])
def fms_gen():
    request = flask.request
    if request.method == 'POST':
        params = get_parameters_from_request(request)
        result = generate_feature_models.delay(params)
        params[Params.TASK_ID.name]['value'] = result.id
        return flask.render_template('config_gen/index.html', params=params)


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
    
