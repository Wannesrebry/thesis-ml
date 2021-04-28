import json

import flask
import requests
from flask_cors import CORS
import os
app = flask.Flask(__name__, static_url_path='/static', static_folder='upload')

app.config["DEBUG"] = True
cors = CORS(app)


def authenticate(request):
    try:
        token_id = request.headers.get("Authorization").split("Bearer ")[1]
        user = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token_id}")
        if not user.ok:
            raise Exception("Authorization token is invalid")
        return user, 200
    except Exception as ex:
        return str(ex), 401


@app.route("/api/test-auth", methods=["GET"])
def test_auth():
    user, user_status_code = authenticate(flask.request)
    if user_status_code != 200:
        return str(user), 401
    return str(user.content.decode()), 200


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
                        ), 200
                except Exception as ex:
                    return flask.jsonify(Message='Projectname is already in use'), 400
            return flask.jsonify(Message='No file found'), 400
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run()
