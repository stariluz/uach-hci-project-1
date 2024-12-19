from student import Student
from marks import Marks

marks = Marks(82, 74)
student = Student(1, "Emma", marks)
student_json=student.to_json()
marks_json=marks.to_json()
print(student_json, marks_json)

print(
    Student.json_to_object(student_json),
    Marks.json_to_object(marks_json)
)