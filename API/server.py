import json

import flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = flask.Flask(__name__, static_url_path='/static', static_folder='upload')
app.config["DEBUG"] = True
cors = CORS(app)


@app.route('/', methods=["GET"])
def home():
    return flask.jsonify({
        "test": "sfdsqfsqddsf"
    }, status=200)


@app.route('/api/projects', methods=["GET"])
def get_projects():
    try:
        dirname = './upload'
        dirs = os.listdir(dirname)
        return flask.jsonify(Dirs=dirs)
    except Exception as ex:
        return ex


@app.route('/api/new', methods=['GET', 'POST'])
def upload_initial_train_data():
    try:
        request = flask.request
        if request.method == 'POST':
            f = request.files['file']
            project_name = request.values.get('name')
            if f:
                try:
                    os.mkdir(f'./upload/{project_name}')
                    f.save(os.path.join(f"./upload/{project_name}", 'upload_train.csv'))
                    return flask.jsonify(
                        ProjectName=project_name,
                        Message="Project Creation was successful"
                        , status=200)
                except Exception as ex:
                    return flask.jsonify(Message='Projectname is already in use', status=400)
            return flask.jsonify(Message='No file found', status=400)
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run()
