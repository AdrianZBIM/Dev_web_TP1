#!/usr/bin/env python3
# coding: utf-8

import functools
import sqlite3

from flask import g, current_app as app


DATABASE = 'database.db'


def userformat(func):
    """user decorator"""
    @functools.wraps(func)
    def wrapper(user):
        app.logger.debug('formating user decorator: %s' % user)
        db_user = get_user(user)
        if db_user and 'id' not in user:
            # update user with itss id if it exists
            user['id'] = db_user['id']
        if 'gender' in user:
            genderid = dict(query_db('SELECT gender.name, gender.id FROM gender;'))
            ug = user.get('gender')
            if ug in genderid:
                user['gender'] = genderid.get(ug)
        return func(user)
    return wrapper


def get_users(uname=None):
    """Query the full list of users as a list of dict
    >>> users = get_users()

    Get a single user (with kwargs uname) as a single user as a dict
    >>> user = get_users({'name': 'Alan Turing'})

    For debug, call with context
    >>> import app
    >>> with app.app.app_context():
    >>>     print(dbmgmt.get_users())
    >>>     print(dbmgmt.get_users({'name': 'Alan Turing'}))
    """
    if uname:
        # Single user request on users.name
        sql = """select users.id, users.name, users.birth, users.wikiid,
        gender.name as gender from users
        INNER JOIN gender ON gender.id = users.gender_id
        WHERE users.name = :name;"""
        user = query_db(sql, uname, one=True)
        if not user:
            return None
        user = dict(user)
        user['fields'] = get_fields(user['id'])
        return user
    # Request all artists
    users = []
    sql = """select users.id, users.name, users.birth, users.wikiid, gender.name
    as gender from users INNER JOIN gender ON gender.id = users.gender_id;"""
    for suser in query_db(sql):
        user = dict(suser)
        user['fields'] = get_fields(user['id'])
        users.append(user)
    return users


def get_user(user):
    """Fetch a user fro DB
    >>> user_id = get_user({'name': 'username'})
    """
    sql = """select users.id from users where name = :name;"""
    return query_db(sql, user, one=True)


@userformat
def add_user(user):
    """Add user, return db user id (primary key in users table).
    Takes as argument a dict with 'name', 'birth', 'gender' keys.
    Function is idempotent.

    >>> dbid = add_user({'name': 'user name', 'birth': 'yyyy-mm-dd',
                         'gender': 'm|f' })
    """
    sql = """INSERT INTO users VALUES (NULL, :name, NULL, :birth, :gender);"""
    db_user = get_user(user)
    app.logger.debug('got :%s' % user)
    if not db_user:
        query_db(sql, user, one=True, save=True)
        db_user = get_user(user)
    return db_user['id']


@userformat
def mod_user(user):
    """Modify a user entry.
    Takes the same argument as add_user:

    >>> mod_user({'name': 'user name', 'birth': 'yyyy-mm-dd',
                  'gender': 'm|f' })
    """
    db_user = get_user(user)
    if not db_user:
        raise Exception('User not found')
    sql = """UPDATE users SET name=:name,birth=:birth,gender_id=:gender WHERE users.id=:id"""
    query_db(sql, user, one=True, save=True)


def get_fields(user_id=None):
    if user_id:
        sql = """SELECT field.user_id, fieldname.name FROM field JOIN fieldname
                 WHERE field.field_id == fieldname.id AND field.user_id == ?;"""
        rv = query_db(sql, [user_id])
        return [f['name'] for f in rv]
    fields = [f['name'] for f in query_db('SELECT name FROM fieldname;')]
    return fields


def query_db(query, args=(), one=False, save=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    if save:
        conn.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

def init_db():
    from os.path import exists as pexists
    if pexists(DATABASE):
        return
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Script starts here
if __name__ == '__main__':
    init_db()

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
