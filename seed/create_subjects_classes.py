# SEQUENCE: 2
from dash.models import CompulsarySubject, OptionalSubject, Classroom
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    try:
        # ========== GRADE 10 Classes ==========
        c1 = Classroom(classroom_name="10A")
        c2 = Classroom(classroom_name="10B")
        c3 = Classroom(classroom_name="10C")
       
        # ========== GRADE 11 Classes ==========
        c4 = Classroom(classroom_name="11A")
        c5 = Classroom(classroom_name="11B")
        c6 = Classroom(classroom_name="11C")

        # ========== GRADE 12 Classes ==========
        c7 = Classroom(classroom_name="12A")
        c8 = Classroom(classroom_name="12B")
        c9 = Classroom(classroom_name="12C")

        # Commit classrooms first to generate IDs
        db.session.add_all([c1, c2, c3,c4,c5,c6,c7,c8,c9])
        db.session.commit()

        # ========== GRADE 10 Compulsory Subjects ==========
        cs1 = CompulsarySubject(
            subject_name="Junior Mathematics 10", 
            subject_code="MAT10"
            )
        cs2 = CompulsarySubject(
            subject_name="English Language 10",
            subject_code="ENG10"
            )
        cs3 = CompulsarySubject(
            subject_name="Science (Integrated) 10", 
            subject_code="SCI10"
            )
        cs4 = CompulsarySubject(
            subject_name="Social Studies 10", 
            subject_code="SOC10"
            )
        cs5 = CompulsarySubject(
            subject_name="Religious Education 10", 
            subject_code="REL10"
            )

        db.session.add_all([cs1, cs2, cs3, cs4, cs5])
        db.session.commit()

        # Link compulsory subjects to classrooms (many-to-many)
        c1.compulsary_subjects.extend([cs1, cs2, cs3, cs4, cs5])
        c2.compulsary_subjects.extend([cs1, cs2, cs3, cs4, cs5])
        c3.compulsary_subjects.extend([cs1, cs2, cs3, cs4, cs5])

        db.session.commit()


        # ========== GRADE 11 Compulsory Subjects ==========
        cs6 = CompulsarySubject(
            subject_name="Basic Mathematics 11", 
            subject_code="MAT11"
            )
        cs7 = CompulsarySubject(
            subject_name="English Language 11",
            subject_code="ENG11"
            )
        cs8 = CompulsarySubject(
            subject_name="Science 11", 
            subject_code="SCI11"
            )
        cs9 = CompulsarySubject(
            subject_name="Social Studies 11", 
            subject_code="SOC11"
            )
        cs10 = CompulsarySubject(
            subject_name="Biolog 11", 
            subject_code="BIO11"
            )

        db.session.add_all([cs6, cs7, cs8, cs9, cs10])
        db.session.commit()

        # Link compulsory subjects to classrooms (many-to-many)
        c4.compulsary_subjects.extend([cs6, cs7, cs8, cs9, cs10])
        c5.compulsary_subjects.extend([cs6, cs7, cs8, cs9, cs10])
        c6.compulsary_subjects.extend([cs6, cs7, cs8, cs9, cs10])

        db.session.commit()

        # ========== GRADE 12 Compulsory Subjects ==========
        cs11 = CompulsarySubject(
            subject_name="Advanced Mathematics 12", 
            subject_code="MAT12"
            )
        cs12 = CompulsarySubject(
            subject_name="English Language 12",
            subject_code="ENG12"
            )
        cs13 = CompulsarySubject(
            subject_name="Science 12", 
            subject_code="SCI12"
            )
        cs14 = CompulsarySubject(
            subject_name="Social Studies 12", 
            subject_code="SOC12"
            )
        cs15 = CompulsarySubject(
            subject_name="Biolog 12", 
            subject_code="BIO12"
            )

        db.session.add_all([cs11, cs12, cs13, cs14, cs15])
        db.session.commit()

        # Link compulsory subjects to classrooms (many-to-many)
        c7.compulsary_subjects.extend([cs11, cs12, cs13, cs14, cs15])
        c8.compulsary_subjects.extend([cs11, cs12, cs13, cs14, cs15])
        c9.compulsary_subjects.extend([cs11, cs12, cs13, cs14, cs15])

        db.session.commit()

        # ========== GRADE 10 Optional Subjects ==========
        ops1 = OptionalSubject(
            subject_name="French 10", 
            subject_code="FRE10", 
            classroom_id=c1.id
            )
        ops2 = OptionalSubject(
            subject_name="Agriculture 10", 
            subject_code="AGR10", 
            classroom_id=c1.id
            )
        ops3 = OptionalSubject(
            subject_name="Business Studies 10", 
            subject_code="BUS10", 
            classroom_id=c2.id
            )
        ops4 = OptionalSubject(
            subject_name="Computer Studies 10", 
            subject_code="COM10", 
            classroom_id=c2.id
            )
        ops5 = OptionalSubject(
            subject_name="CIVIC 10", 
            subject_code="CVC10", 
            classroom_id=c3.id
            )
        ops6 = OptionalSubject(
            subject_name="Geography 10",
            subject_code="GEO10", classroom_id=c3.id)

        db.session.add_all([ops1, ops2, ops3, ops4, ops5, ops6])
        db.session.commit()

        # ========== GRADE 11 Optional Subjects ==========
        ops7 = OptionalSubject(
            subject_name="RELIGOUS EDUCATION 11", 
            subject_code="RE11", 
            classroom_id=c4.id
            )
        ops8 = OptionalSubject(
            subject_name="FOOD & NUTRITUTION 11", 
            subject_code="FN11", 
            classroom_id=c4.id
            )
        ops9 = OptionalSubject(
            subject_name="HISTORY 11", 
            subject_code="HIS11",
            classroom_id=c5.id
            )
        ops10 = OptionalSubject(
            subject_name="COMPUTER SCIENCE 11", 
            subject_code="CS11", 
            classroom_id=c5.id
            )
        ops11 = OptionalSubject(
            subject_name="CIVIC 11", 
            subject_code="CVC11", 
            classroom_id=c6.id
            )
        ops12 = OptionalSubject(
            subject_name="GEOGRAPHY 11", 
            subject_code="GEO11", 
            classroom_id=c6.id
            )

        db.session.add_all([ops7, ops8, ops9, ops10, ops11, ops12])
        db.session.commit()

        # ========== GRADE 12 Optional Subjects ==========
        ops13 = OptionalSubject(
            subject_name="RELIGOUS EDUCATION 12", 
            subject_code="RE12", 
            classroom_id=c7.id
            )
        ops14 = OptionalSubject(
            subject_name="FOOD & NUTRITUTION 12", 
            subject_code="FN12", 
            classroom_id=c7.id
            )
        ops15 = OptionalSubject(
            subject_name="HISTORY 12", 
            subject_code="HIS12", 
            classroom_id=c8.id
            )
        ops16 = OptionalSubject(
            subject_name="COMPUTER SCIENCE 12", 
            subject_code="CS12", 
            classroom_id=c8.id
            )
        ops17 = OptionalSubject(
            subject_name="CIVIC 12", 
            subject_code="CVC12", 
            classroom_id=c9.id
            )
        ops18 = OptionalSubject(
            subject_name="GEOGRAPHY 12", 
            subject_code="GEO12", 
            classroom_id=c9.id
            )

        db.session.add_all([ops7, ops8, ops9, ops10, ops11, ops12])
        db.session.commit()



        print("Subjects and classes for Grade 10,11,12 created successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
