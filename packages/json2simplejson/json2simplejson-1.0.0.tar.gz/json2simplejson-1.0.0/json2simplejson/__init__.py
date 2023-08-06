import json
import simplejson


def patch():
    """Monkey patches all of the needed functions in the json library"""
    json.dump = simplejson.dump
    json.dumps = simplejson.dumps
    json.load = simplejson.load
    json.loads = simplejson.loads
    json.JSONDecoder = simplejson.JSONDecoder
    json.JSONEncoder = simplejson.JSONEncoder
