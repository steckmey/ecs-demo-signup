# Copyright 2015. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json

import flask
from flask import request, Response

from redis import Redis

# Create the Flask app
application = flask.Flask(__name__)
redis = Redis(host='redis', port=6379)

@application.route('/')
def welcome():
    return flask.render_template('index.html')

@application.route('/signup', methods=['POST'])
def signup():
    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    if redis.exists(signup_data['email']):
        return Response("", status=409, mimetype='application/json')
    else:
        redis.set(signup_data['email'], 'true')

    return Response(json.dumps(signup_data), status=201, mimetype='application/json')

if __name__ == '__main__':
    application.run(host='0.0.0.0')
