from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from faker import Faker
from random import randint
from faker.providers import BaseProvider


db = SQLAlchemy()
migrate = Migrate()
faker = Faker()

class CustomIDGenerator(BaseProvider):
    def generate_teacher_id(self):
        return f"{randint(1000,9999)}"

    def generate_student_id(self):
        return f"{randint(1000,9999)}"

# Register provider
faker.add_provider(CustomIDGenerator)