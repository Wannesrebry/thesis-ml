import json
import time
from collections import namedtuple
import flask
import requests
from flask_cors import CORS
import os
from user import *
app = flask.Flask(__name__, static_url_path='/static', static_folder='upload')

app.config["DEBUG"] = True
cors = CORS(app)


def authenticate(request):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise Exception('No Bearer token found')
        token_parts = token.split(" ")
        if not len(token_parts) == 2:
            raise Exception("Invalid Token")
        token_id = token_parts[1]  # ['Bearer', '{token_id}']
        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token_id}")
        if not response.ok:
            raise Exception("Authorization token is invalid")
        return GoogleUser(response), 200
    except Exception as ex:
        return str(ex), 401


@app.route("/api/test-auth", methods=["GET"])
def test_auth():
    user, user_status_code = authenticate(flask.request)
    if user_status_code != 200:
        return str(user), 401
    return user.json(), 200


@app.route('/api/projects', methods=["GET"])
def get_projects():
    user, user_status_code = authenticate(flask.request)
    if user_status_code != 200:
        return str(user), 401
    try:
        dirname = f'./upload/{user.email}'
        dirs = os.listdir(dirname)
        return flask.jsonify(Dirs=dirs), 200
    except Exception as ex:
        return flask.jsonify(Dirs=[]), 200


@app.route('/api/new', methods=['GET', 'POST'])
def upload_initial_train_data():
    try:
        # Auth
        user, user_status_code = authenticate(flask.request)
        if user_status_code != 200:
            return str(user), 401
        # --
        request = flask.request
        if request.method == 'POST':
            f = request.files['file']
            user_email = user.email
            project_name = request.values.get('name')
            user_projects_path = f'./upload/{user_email}'
            if f:
                try:
                    os.mkdir(user_projects_path)
                except Exception as ex:
                    pass
                try:
                    os.mkdir(f'{user_projects_path}/{project_name}')
                    f.save(os.path.join(f"{user_projects_path}/{project_name}", 'upload_train.csv'))
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
