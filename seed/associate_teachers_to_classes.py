from auth.models import TeacherSchoolRecord
from dash.models import Classroom,teacherschoolrecord_classroom
from app import create_app
from extensions import db


# get all teacher records
all_teacher_records = TeacherSchoolRecord.query.all()
print(all_teacher_records)
# get all classrooms
all_classrooms = Classroom.query.all()
print(all_classrooms)
