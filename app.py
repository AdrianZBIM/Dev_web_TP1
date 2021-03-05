#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, url_for, g
from flask import abort, request, make_response
from flask import render_template
from markupsafe import escape

from dbmgmt import get_users, add_user, mod_user

# Set API dev in an another file
from api import SITE_API

HELLO_STRINGS = {
        "cn": "你好世界\n",
        "du": "Hallo wereld\n",
        "en": "Hello world\n",
        "fr": "Bonjour monde\n",
        "de": "Hallo Welt\n",
        "gr": "γειά σου κόσμος\n",
        "it": "Ciao mondo\n",
        "jp": "こんにちは世界\n",
        "kr": "여보세요 세계\n",
        "pt": "Olá mundo\n",
        "ru": "Здравствуй, мир\n",
        "sp": "Hola mundo\n"
}


## START: DO NOT MODIFY THIS PART ##
app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)


@app.teardown_appcontext
def close_connection(exception):
    # manage database tear down
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
## END: DO NOT MODIFY THIS PART ##


@app.route('/hello_world')
def hello_world():
    app.logger.debug('Hello world')
    app.logger.debug('Here is the request I got: {}'.format(request))
    app.logger.debug('Here is the headers I got: {}'.format([k for k in request.headers.keys()]))
    app.logger.debug(request.headers["Accept-Language"][0:2])
    if request.headers["Accept-Language"] and request.headers["Accept-Language"][0:2] in HELLO_STRINGS:
    	resp = make_response(HELLO_STRINGS[request.headers["Accept-Language"][0:2]])
    	resp.headers["Content-Language"] = request.headers["Accept-Language"]
    	
    else:
    	resp = make_response(HELLO_STRINGS["en"])
    resp.headers["Content-Type"] = "text/plain"
    resp.headers["X-Less"] = "Is More"
    #abort(404)
    return resp, 1312


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/about')
def about():
    from datetime import datetime
    today = datetime.today()
    app.logger.debug('about')
    # Create a context
    tpl_context = {}
    # Populate a context to feed the template
    # (cf. http://strftime.org/ for string formating with datetime)
    tpl_context.update({'day': '{:%A}'.format(today)})
    tpl_context.update({'d_o_month': '{:%d}'.format(today)})
    tpl_context.update({'month': '{:%B}'.format(today)})
    tpl_context.update({'time': '{:%X}'.format(today)})
    tpl_context.update({'date': today})
    # Now let's see how the context looks like
    app.logger.debug('About Context: {}'.format(tpl_context))
    return render_template('about.html', page_title = "About page", context=tpl_context)


@app.route('/users')

@app.route('/users/<username>/')
def users(username=None):
	app.logger.debug(username, "nom renvoyé")
	app.logger.debug(get_users({"name": username}))
	if (not username):
		dic_user = get_users()
		app.logger.debug("on entre dans username global")
		return render_template("users.html", page_title = "Users",  username = username, dic_user = dic_user)
	elif get_users({"name": username}):
		app.logger.debug("on entre dans username spécifique")
		username = get_users({"name": username})
		return render_template("users.html", page_title = username['name'],  username = username)
	else:
		abort(404, "Pas d'user avec le nom donné")


@app.route('/search/', methods=['GET'])
def search():
	app.logger.debug(request.args)
	app.logger.debug(request.args["pattern"])
	if get_users({"name": request.args["pattern"]}):
		trouve = get_users({"name": request.args["pattern"]})
	else:
		trouve = None
	return render_template("users.html", page_title = request.args["pattern"], trouve = trouve,  search = request.args["pattern"])
	# Script starts here
if __name__ == '__main__':
    from dbmgmt import init_db
    init_db()
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
