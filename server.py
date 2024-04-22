
from flask import Flask, views, jsonify, send_file, request
from celery import Celery
from upscale import upscale
from celery.result import AsyncResult
import celery


app_name = 'upscale_app'
app = Flask(app_name)



class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery = Celery(
    app_name,
    backend='redis://localhost:6379/1',
    broker='redis://localhost:6379/2',
    broker_connection_retry_on_startup=True,
    task_cls=ContextTask
)



@celery.task(name='upscale_app.upscale_image')
def upscale_image(input_path, output_path):
    result = upscale(input_path, output_path)
    return result


class Upscale(views.MethodView):

    def __init__(self):
        self.host = 'http://127.0.0.1:5000'


    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        if task.status == 'SUCCESS':
            return jsonify({'status': task.status,
                            'link': f'{self.host}/processed/{task.result}'
                            })

        return jsonify({'status': task.status})


    def post(self):
        image_paths = request.get_json()
        input_image_path = image_paths.get('image_1')
        output_image_path = image_paths.get('image_2')
        task = upscale_image.delay(input_image_path, output_image_path)
        return jsonify({'task_id': task.id})



class Image(views.MethodView):

    def get(self, file):
        file = send_file(file, mimetype=None, as_attachment=False)
        return file



upscale_view = Upscale.as_view('upscale')
image_view = Image.as_view('image')
app.add_url_rule('/tasks/<string:task_id>', view_func=upscale_view, methods=['GET'])
app.add_url_rule('/upscale/', view_func=upscale_view, methods=['POST'])
app.add_url_rule('/processed/<string:file>', view_func=image_view, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)


