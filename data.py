# coding: utf-8
"""App data

Get wiki page ID: https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Page%20Title
Get a thumbnail : https://en.wikipedia.org/w/api.php?action=query&titles=Alan%20Turing&prop=pageimages&format=json&pithumbsize=100
"""

import json

from datetime import date, datetime

with open('data.json') as js:
    DATA = json.load(js)
    USERS = DATA.get('USERS')
    FIELDS = DATA.get('FIELDS')

def get_fields(u_id):
    for field, ids in FIELDS.items():
        if u_id in ids:
            yield field


for user in USERS:
    user.update({'fields': [f for f in get_fields(user.get('id'))]})

# Script starts here
if __name__ == '__main__':
    pass

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
