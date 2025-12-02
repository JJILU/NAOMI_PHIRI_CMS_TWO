from auth.models import StudentSchoolRecord
from dash.models import StudentGrade,Classroom
from extensions import db
from app import create_app
from random import choices


app = create_app()


with app.app_context():
    all_students = StudentSchoolRecord.query.all()

    for student in all_students:

        student_classroom = student.classroom  # correct way
        
        if not student_classroom:
            print("Student has no classroom. Skipping…")
            continue

        cs_list = student_classroom.compulsary_subjects
        op_list = student_classroom.optional_subjects

        # both lists must have at least 1 subject
        if not cs_list or not op_list:
            print("Student classroom has no subjects. Skipping…")
            continue

        # generate equal weights
        com_weights = [1] * len(cs_list)
        op_weights = [1] * len(op_list)

        # pick one compulsory & one optional
        com_subject = choices(cs_list, weights=com_weights, k=1)[0]
        optional = choices(op_list, weights=op_weights, k=1)[0]

        # now select from the two picked subjects
        exam_subject = choices([com_subject, optional], weights=[50, 50], k=1)[0]

        print("Compulsory:", com_subject.subject_name)
        print("Optional:", optional.subject_name)
        print("Exam Subject Selected:", exam_subject.subject_name)
        print("----")

        for _ in range(10):
            score = choices([45,22,78,98], weights=[5,10,60,25])[0]

            if score > 90:
                grade = "A+"
            elif score > 60:
                grade = "B+"
            elif score > 40:
                grade = "C"
            elif score > 20:
                grade = "D"
            else:
                grade = "F"

            new_grade = StudentGrade(
                exam_name=f"{exam_subject.subject_name} Exam",
                exam_code=exam_subject.subject_code,
                exam_subject_name=exam_subject.subject_name,
                student_grade=grade,
                student_score=score,
                student_school_record_id=student.id
            )

            db.session.add(new_grade)

        db.session.commit()

