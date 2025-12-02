from auth.models import TeacherSchoolRecord
from dash.models import CompulsarySubject,OptionalSubject
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
  # get all teacher records
  all_teacher_records = TeacherSchoolRecord.query.all()
  print(all_teacher_records)
  # get all classrooms
  all_classrooms = CompulsarySubject.query.all()
  print(all_classrooms)
