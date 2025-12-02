from dash.models import Classroom
from auth.models import StudentSchoolRecord,Student,Admin
from app import create_app
from extensions import db,faker
from faker.providers import BaseProvider
from random import choices,choice

# init app
flask_app = create_app()

# get all classes
def get_classes():
    all_classroom = Classroom.query.all()
    return all_classroom


def create_student_school_records():
    for _ in range(10):
        # generate randomly is_admin value
        is_admin = choices([True,False],weights=[20,80])[0]  
        student_class = choice(get_classes())
        new_student = StudentSchoolRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            card_id=faker.generate_student_id(),
            is_admin=is_admin,
            classroom_id=student_class.id
        )
        db.session.add(new_student)
    db.session.commit()      



with flask_app.app_context():
    try:
        create_student_school_records()
        print(f" Students created successfully")
    except Exception as e:
        print(f"Failed to create teachers & students error occured {str(e)}")
        
            




