from json_class import JsonClass
from marks import Marks

class Student(JsonClass):
    def __init__(self, rollNumber, name, marks):
        self.rollNumber, self.name, self.marks = rollNumber, name, marks

    def json_to_object(json_object):
        object=Student.json_to_tuple(json_object)
        return Student(
            object.rollNumber,
            object.name,
            Marks(
                object.marks["english"], object.marks["geometry"]
            )
        )
