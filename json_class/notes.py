from json_class import JsonClass

class Notes(JsonClass):
    def __init__(self, english, geometry):
        self.english, self.geometry = english, geometry

    def json_to_object(json_object):
        object=Notes.json_to_tuple(json_object)
        return Notes(
            object.english, object.geometry
        )