from typing import Any 
import shutil

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
    print(f'/update_progress')
    result = AsyncResult(task_id)
    if result.ready():
        print(f'result.ready')
        # Task has completed
        if result.successful():
            data = 'data: 100\n\n'
            return flask.Response(data, mimetype="text/event-stream")
        else:
            # Task completed with an error
            #sse.publish({"message": "Hello!"}, type='greeting')
            return flask.jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        print(f'result.pending')
        # Task is still pending
        # Get percentage
        data = 'data: 50\n\n'
        return flask.Response(data, mimetype="text/event-stream")
    

@config_gen_bp.route("/get_result/<task_id>", methods=['GET'])
def task_result(task_id) -> dict[str, object]:
    print(f'/get_result')
    print(f'/result_id {task_id}')
    result = AsyncResult(task_id)
    if result.ready():
        print(f'result.ready')
        # Task has completed
        if result.successful():
            params = result.result
            temp_zipfile = params[Params.ZIP_FILE.name]['value']
            zip_filename = params[Params.ZIP_FILENAME.name]['value']
            print(f'zip.file: {temp_zipfile}')
            print(f'zip.zip_filename: {zip_filename}')
            print(f'SERIALIZATION_TEMPORAL_DIR: {params[Params.SERIALIZATION_TEMPORAL_DIR.name]["value"]}')
            response = flask.make_response(flask.send_file(path_or_file=temp_zipfile, 
                                                           as_attachment=True, 
                                                           download_name=zip_filename))
            return response
        else:
            # Task completed with an error
            #sse.publish({"message": "Hello!"}, type='greeting')
            return flask.jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        # Task completed with an error
        #sse.publish({"message": "Hello!"}, type='greeting')
        return flask.jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    

# def generate():
#     x = 0
#     while x <= 100:
#         yield "event: progress_bar\ndata:" + str(x) + "\n\n"
#         x = x + 10
#         time.sleep(0.5)


# def stream_template(template_name, **context):
#     flask.current_app.update_template_context(context)
#     t = flask.current_app.jinja_env.get_template(template_name)
#     rv = t.stream(context)
#     rv.enable_buffering(5)
#     return rv

# @config_gen_bp.route('/progress')
# def progress():
#     if flask.request.method == 'GET':    
#         #data = generate_feature_models(params)
#         #return flask.current_app.response_class(stream_template('config_gen/index.html', data=data), mimetype='text/event-stream')
#         return flask.Response(generate(), mimetype='text/event-stream')
#         #return flask.Response(generate_feature_models(params), mimetype='text/event-stream')


@config_gen_bp.route('/fmsGen', methods=['POST'])
def fms_gen():
    request = flask.request
    if request.method == 'POST':
        params = get_parameters_from_request(request)
        #return flask.Response(generate(), mimetype='text/event-stream')
        # Generate random feature models
        #params[Params.SERIALIZATION_TEMPORAL_DIR.name] = Params.SERIALIZATION_TEMPORAL_DIR.value.to_dict()
        #params[Params.SERIALIZATION_TEMPORAL_DIR.name]['value'] = temp_dir
        print(f'Generate feature models...')
        result = generate_feature_models.delay(params)
        print(f'Generate feature models (done!)')
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
    
