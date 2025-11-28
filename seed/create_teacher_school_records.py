from extensions import db,faker
from auth.models import TeacherSchoolRecord,Teacher
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


# get all classes
def get_classes():
    all_teachers = TeacherSchoolRecord.query.all()
    print(all_teachers)


with flask_app.app_context():
    # db.create_all()
    try:
        # create students school records
        # create_teacher_school_records()
        # print(f"Teachers created successfully")
        get_classes()
    except Exception as e:
        print(f"Failed to create teachers & students error occured {str(e)}")
        
            

