from dash.models import Classroom
from auth.models import StudentSchoolRecord,Student,Admin
from app import create_app
from extensions import db,faker
from faker.providers import BaseProvider
from random import choices

# init app
flask_app = create_app()

# get all classes
def get_classes():
    pass


def create_student_school_records():
    for _ in range(10):
        # generate randomly is_admin value
        is_admin = choices([True,False],weights=[10,90])[0]  
        # student_class = random.choice()
        new_student = StudentSchoolRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            card_id=faker.student_id(),
            is_admin=is_admin
        )
        db.session.add(new_student)
    db.session.commit()      



with flask_app.app_context():
    # db.create_all()
    try:
        create_student_school_records()
        print(f" Students created successfully")
    except Exception as e:
        print(f"Failed to create teachers & students error occured {str(e)}")
        
            




