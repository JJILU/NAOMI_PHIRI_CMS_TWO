from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from faker import Faker
from random import randint
from faker.providers import BaseProvider
from flask_socketio import SocketIO


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
faker = Faker()
socketio = SocketIO()

class CustomIDGenerator(BaseProvider):
    def generate_teacher_id(self):
        return f"T{randint(1000,9999)}"

    def generate_student_id(self):
        return f"S{randint(1000,9999)}"

# Register provider
faker.add_provider(CustomIDGenerator)