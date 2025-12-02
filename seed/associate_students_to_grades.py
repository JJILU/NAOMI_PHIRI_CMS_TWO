from auth.models import StudentSchoolRecord
from dash.models import Classroom
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
  # get all teacher records
  all_student_records = StudentSchoolRecord.query.all()
  print(all_student_records)
  # get all classrooms
  all_classrooms = Classroom.query.all()
  print(all_classrooms)