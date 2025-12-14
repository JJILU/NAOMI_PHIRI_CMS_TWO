from auth.models import StudentSchoolRecord
from dash.models import StudentAttendance
from extensions import db
from app import create_app
from random import choices
from datetime import date, timedelta
import random

app = create_app()

with app.app_context():
    # get all students 
    all_students = StudentSchoolRecord.query.all()
    print(f"Found {len(all_students)} students.")

    try:
        for student in all_students:
            # create multiple attendance records per student (optional)
            for i in range(5):  # e.g., last 5 days
                att_date = date.today() - timedelta(days=i)
                status = choices(["Present", "Absent"], weights=[50, 50])[0]

                new_attendance = StudentAttendance(
                    status=status,
                    attendance_date=att_date,
                    student_school_record_id=student.id
                )

                db.session.add(new_attendance)

        db.session.commit()
        print("Student attendances seeded successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to create student attendances: {str(e)}")
