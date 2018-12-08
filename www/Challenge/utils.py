__author__ = 'carson.qin'

from flask import jsonify

def error_json(errmsg=None):
    return jsonify(ret=False, errmsg=errmsg)

def data_json(data=None):
    return jsonify(ret=True, data=data)

def success_json(msg=None):
    return jsonify(ret=True, msg=msg)
