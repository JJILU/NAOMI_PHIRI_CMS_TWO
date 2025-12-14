# seed/create_teacher_school_records.py
from extensions import db, faker
from auth.models import TeacherSchoolRecord

def create_teacher_school_records():
    """Creates 10 random teacher records."""
    
    try:
        for _ in range(10):
            teacher = TeacherSchoolRecord(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                card_id=faker.generate_teacher_id()
            )
            db.session.add(teacher)
        db.session.commit()
        print("Teacher records created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create teacher records: {e}")
