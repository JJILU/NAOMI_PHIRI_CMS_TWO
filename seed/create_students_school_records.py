# seed/create_students_school_records.py
from extensions import db, faker
from auth.models import StudentSchoolRecord
from dash.models import Classroom
from random import choices, choice

def create_student_school_records():
    """Creates 10 random student records assigned to random classrooms."""
    try:
        classrooms = Classroom.query.all()
        for _ in range(10):
            student_class = choice(classrooms)
            student = StudentSchoolRecord(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                card_id=faker.generate_student_id(),
                is_admin=choices([True, False], weights=[20, 80])[0],
                classroom_id=student_class.id
            )
            db.session.add(student)
        db.session.commit()
        print("Student records created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create student records: {e}")
