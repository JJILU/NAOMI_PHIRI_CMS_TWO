from dash.models import CompulsarySubject,OptionalSubject,Classroom
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    try:
       # GRADE 10 classes
        c1 = Classroom(classroom_name="10A")
        c2 = Classroom(classroom_name="10B")
        c3 = Classroom(classroom_name="10C")

        # GRADE 10 compulsary subjects
        cs1 = CompulsarySubject(subject_name="Mathematics",subject_code="MAT10")
        cs2 = CompulsarySubject(subject_name="English Language",subject_code="ENG10")
        cs3 = CompulsarySubject(subject_name="Science (Integrated)",subject_code="SCI10")
        cs4 = CompulsarySubject(subject_name="Social Studies",subject_code="SOC10")
        cs5 = CompulsarySubject(subject_name="Religious Education",subject_code="REL10")

        # GRADE 10 optional subjects
        ops1 = OptionalSubject(subject_name="French",subject_code="FRE10",classroom_id=c1.id)
        ops2 = OptionalSubject(subject_name="Agriculture",subject_code="AGR10",classroom_id=c1.id)
        ops3 = OptionalSubject(subject_name="Business Studies",subject_code="BUS10",classroom_id=c2.id)
        ops4 = OptionalSubject(subject_name="Computer Studies",subject_code="COM10",classroom_id=c2.id)
        ops5 = OptionalSubject(subject_name="CIVIC",subject_code="CVC10",classroom_id=c3.id)
        ops6 = OptionalSubject(subject_name="GEOGRAPHY SUB10",subject_code="GEO10",classroom_id=c3.id)

        db.session.add_all([c1,c2,c3,cs1,cs2,cs3,cs4,cs5,ops1,ops2,ops3,ops4,ops5,ops6])
        db.session.commit()
        print("subjects and  classes created successfully!")
    except Exception as e:
        print(f"Error occured {e}")    