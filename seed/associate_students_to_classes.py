from auth.models import TeacherSchoolRecord
from dash.models import Classroom
from app import create_app
from extensions import db,faker
from faker.providers import BaseProvider
from random import randint,choice,choices

# init app
flask_app = create_app()

# create custom id generator
class CustomIDGenerator(BaseProvider):
    def generate_teacher_id(self):
        return f"{randint(1000,9999)}"
    def generate_student_id(self):
        return f"{randint(1000,9999)}"




