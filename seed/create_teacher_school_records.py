from extensions import db,faker
from auth.models import TeacherSchoolRecord
from app import create_app


flask_app = create_app()

def create_teacher_school_records():
    for _ in range(10):
        new_teacher = TeacherSchoolRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            card_id=faker.generate_teacher_id()
        )
        db.session.add(new_teacher)
    db.session.commit()   


with flask_app.app_context():
    try:
        # create_teacher_school_records()
        print("created teacher records successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create teachers & students error occured {str(e)}")
        
            

