#!/usr/bin/env python3
"""
server.py -- http api server
========================
Http api server for smg client
Provides auth and notebook api
Validates game state
"""


import sqlite3
from time import time
from uuid import uuid1

from flask import Flask, jsonify, abort, request, make_response, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import database
db_name = "db/mydatabase.db"

APP = Flask(__name__)
AUTH = HTTPBasicAuth()
database.init(sqlite3.connect(db_name))


def dict_factory(cursor, row):
    """Return DB tuple as dict"""

    res = {}
    for idx, col in enumerate(cursor.description):
        res[col[0]] = row[idx]

    return res


def conn_get():
    """Return DB connection, creates connection if needed"""

    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(db_name)
        conn.row_factory = dict_factory

    return conn


@APP.teardown_appcontext
def conn_close(_):
    """Close DB connection"""

    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


@AUTH.error_handler
def forbidden():
    """403 status wrapper"""

    return make_response(jsonify({'error': 'Forbidden'}), 403)


@APP.errorhandler(400)
def bad_request(_):
    """400 status wrapper"""

    return make_response(jsonify({'error': 'Bad Request'}), 400)


@APP.errorhandler(409)
def conflict(_):
    """409 status wrapper"""

    return make_response(jsonify({'error': 'Conflict'}), 409)


@APP.errorhandler(406)
def not_acceptable(_):
    """406 status wrapper"""

    return make_response(jsonify({'error': 'Not Acceptable'}), 406)


@APP.errorhandler(404)
def not_found(_):
    """404 status wrapper"""

    return make_response(jsonify({'error': 'Not Found'}), 404)


@APP.errorhandler(500)
def internal(_):
    """500 status wrapper"""
    return make_response(jsonify({'error': 'Internal Error'}), 500)


@AUTH.verify_password
def verify_password(username, password):
    """Validate password"""

    conn = conn_get()
    user = database.get_user(conn, username)
    if user is None:
        return False

    return check_password_hash(user['password'], password)


@APP.route('/api/v1/health_check', methods=['GET'])
def health_check():
    """
    Api.health_check method
    returns status "ok" or fails
    """
    return jsonify({"status": "ok"})


@APP.route('/api/v1/auth', methods=['GET'])
@AUTH.login_required
def authenticate():
    """
    Api.auth method
    arguments: []
    returns: empty body
    200 -- auth success
    403 -- wrong authorization
    500 -- internal error
    """

    return ""


@APP.route('/api/v1/auth', methods=['POST'])
def register():
    """
    Api.register method
    arguments: [username, password]
    returns: empty body
    201 -- registration success
    400 -- wrong arguments
    409 -- username exists
    500 -- internal error
    """

    if not request.json \
            or not 'username' in request.json or len(request.json['username']) == 0 \
            or not 'password' in request.json or len(request.json['password']) == 0:
        abort(400)

    conn = conn_get()
    user = database.get_user(conn, request.json['username'])
    if user is not None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    database.add_user(conn, user)
    conn.commit()

    return "", 201


@APP.route('/api/v1/note', methods=['PUT'])
@AUTH.login_required
def create_note():
    """
    Api.create_note method
    arguments: [payload]
    returns: [uuid, user, ctime, atime, text, date]
    201 -- note created
    400 -- wrong arguments
    403 -- wrong authorization
    500 -- internal error
    """

    if not request.json or not 'text' in request.json:
        abort(400)

    if not 'date' in request.json:
        request.json["date"] = "0"

    conn = conn_get()
    note = {
        'uuid':  str(uuid1()),
        'user':  AUTH.username(),
        'ctime': int(time()),
        'atime': int(time()),
        'date':  int(request.json["date"]),
	'text':  request.json["text"]
    }
    database.add_note(conn, note)
    conn.commit()

    return jsonify(note), 201


@APP.route('/api/v1/note/<string:uuid>', methods=['GET'])
@AUTH.login_required
def get_note(uuid):
    """
    Api.get_note method
    returns: [uuid, user, ctime, atime, text, date]
    200 -- ok
    400 -- wrong arguments
    403 -- wrong authorization
    404 -- note not found
    500 -- internal error
    """

    conn = conn_get()
    note = database.get_note(conn, uuid)
    if note is None:
        abort(404)

    if AUTH.username() != note["user"]:
        abort(403)

    return jsonify(note)


@APP.route('/api/v1/note/<string:uuid>', methods=['POST'])
@AUTH.login_required
def update_note(uuid):
    """
    Api.make_move method
    arguments: [hash, round, payload]
    returns: empty body
    200 -- note updated
    400 -- wrong arguments
    403 -- wrong authorization
    404 -- note not found
    500 -- internal error
    """

    conn = conn_get()
    note = database.get_note(conn, uuid)
    if note is None:
        abort(404)

    if AUTH.username() != note["user"]:
        abort(403)

    note["atime"] = int(time())
    if request.json and 'text' in request.json:
        note["text"] = request.json["text"]
    if request.json and 'date' in request.json:
        note["date"] = int(request.json["date"])

    database.update_note(conn, note)
    conn.commit()

    return jsonify(note)


if __name__ == '__main__':
    APP.run(debug=False)
