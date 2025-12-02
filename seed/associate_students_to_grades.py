from auth.models import StudentSchoolRecord
from dash.models import StudentGrade
from extensions import db
from app import create_app
from random import choices


app = create_app()


with app.app_context():
    # get all students 
    all_students = StudentSchoolRecord.query.all()
    print(all_students)

    try:
        for student in all_students:
            is_present = choices([True,False],weights=[50,50])[0]
            new_attendance = StudentGrade(
                is_present=is_present,
                student_school_record_id=student.id
            )

            db.session.add(new_attendance)

        db.session.commit()  
    except Exception as e:
        db.session.rollback()
        print(f"failed to create student attendances : {str(e)}")


    

        


