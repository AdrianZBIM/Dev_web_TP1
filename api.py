# coding: utf-8

from flask import request, abort, make_response, current_app
from flask import Blueprint, jsonify

# Database access
from dbmgmt import get_users, add_user, get_user, mod_user

SITE_API = Blueprint('api', __name__,)


@SITE_API.route('/api')
@SITE_API.route('/api/<string:node0>', methods=['GET', 'POST'])
def api(node0=None):
    current_app.logger.debug('Looking at "{}" resource'.format(node0))
    abort(501)


@SITE_API.route('/api/users', methods=['GET', 'POST'])
@SITE_API.route('/api/users/<username>/')
def users_api(username = None):
	if request.args:
		if request.args.get("gender"):
			return jsonify(get_users({"gender": request.args.get("gender")}))
		if request.args.get("name"):
			return jsonify(get_users({"name": request.args.get("name")}))
	else:
		if (not username):
			dic_user = get_users()
			return jsonify(dic_user)
		elif get_users({"name": username}):
			username = get_users({"name": username})
			return jsonify(username)
		else:
			abort(404, "Pas d'user avec le nom donné")


# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
