from extensions import db,faker
from auth.models import TeacherSchoolRecord,StudentSchoolRecord,Teacher,Admin,Student
from faker.providers import BaseProvider
from app import create_app
import random



flask_app = create_app()


# create custom providers
class CustomIDProviders(BaseProvider):
    def teacher_id(self):
        return f"T{random.randint(1000,9999)}"
    def student_id(self):
        return f"S{random.randint(1000,9999)}"

  
    

faker.add_provider(CustomIDProviders)


# def create_teacher_school_records():
#     for _ in range(10):
#         new_teacher = TeacherSchoolRecord(
#             first_name=faker.first_name(),
#             last_name=faker.last_name(),
#             card_id=faker.teacher_id()
#         )
#         db.session.add(new_teacher)
#     db.session.commit()   

def create_student_school_records():
    for _ in range(10):
        # generate randomly is_admin value
        is_admin = random.choices([True,False],weights=[10,90])[0]  
        new_student = StudentSchoolRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            card_id=faker.student_id(),
            is_admin=is_admin
        )
        db.session.add(new_student)
    db.session.commit()      




with flask_app.app_context():
    db.create_all()
    
    try:
        # create_teacher_school_records()
        # print(f"Teachers created successfully")
        create_student_school_records()
        print(f" Students created successfully")
    except Exception as e:
        print(f"Failed to create teachers & students error occured {str(e)}")
        
            

