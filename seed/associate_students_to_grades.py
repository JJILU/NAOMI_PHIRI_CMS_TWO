from auth.models import StudentSchoolRecord
from dash.models import StudentGrade,Classroom
from extensions import db
from app import create_app
from random import choices


app = create_app()


with app.app_context():
    all_students = StudentSchoolRecord.query.all()

    for student in all_students:

        # the correct classroom
        student_classroom = student.classroom  

        if not student_classroom:
            print("Student has no classroom. Skipping…")
            continue

        cs_list = student_classroom.compulsary_subjects
        op_list = student_classroom.optional_subjects

        # skip empty lists
        if not cs_list or not op_list:
            print("Subjects missing. Skipping...")
            continue

        com_weights = [1] * len(cs_list)
        op_weights = [1] * len(op_list)

        com_subject = choices(cs_list, weights=com_weights, k=1)[0]
        optional = choices(op_list, weights=op_weights, k=1)[0]

        print(com_subject, optional)
