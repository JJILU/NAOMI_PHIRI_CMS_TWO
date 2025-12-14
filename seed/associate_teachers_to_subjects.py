# seed/associate_teachers_subjects.py
from extensions import db
from auth.models import TeacherSchoolRecord
from dash.models import CompulsarySubject, OptionalSubject
from random import choice

def associate_teachers_to_subjects():
    """Associate teachers to subjects randomly."""
    try:
        all_compulsary_subjects = CompulsarySubject.query.all()
        all_optional_subjects = OptionalSubject.query.all()
        all_teachers = TeacherSchoolRecord.query.all()

        if not all_teachers:
            print("No teachers found. Skipping association.")
            return

        # Assign random teachers to compulsary subjects
        for cs in all_compulsary_subjects:
            teacher = choice(all_teachers)
            cs.teacherschoolrecords.append(teacher)

        # Assign random teachers to optional subjects
        for os in all_optional_subjects:
            teacher = choice(all_teachers)
            os.teacherschoolrecords.append(teacher)

        db.session.commit()
        print("Successfully associated teachers to subjects.")

        # Optional: print sample teacher-subject association
        sample_teacher = TeacherSchoolRecord.query.first()
        if sample_teacher:
            print("Sample teacher associations:")
            print("Compulsary subjects:", sample_teacher.compulsarysubject)
            print("Optional subjects:", sample_teacher.optionalsubject)

    except Exception as e:
        db.session.rollback()
        print(f"Failed to associate teachers to subjects: {str(e)}")
