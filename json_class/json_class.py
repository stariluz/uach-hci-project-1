import json
from collections import namedtuple
# from json import JSONEncoder

class BaseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class JsonClass:
    def to_json(self):
        return json.dumps(self, indent=4, cls=BaseEncoder)
    
    def json_to_object(json_object):
        return json.loads(json_object)
    
    def object_to_tuple(object):
        return namedtuple('X', object.keys())(*object.values())
    
    def json_to_tuple(json_object):
        return JsonClass.object_to_tuple(JsonClass.json_to_object(json_object))
