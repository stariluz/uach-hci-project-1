from json_class import JsonClass

class Marks(JsonClass):
    def __init__(self, english, geometry):
        self.english, self.geometry = english, geometry

    def json_to_object(json_object):
        object=Marks.json_to_tuple(json_object)
        return Marks(
            object.english, object.geometry
        )