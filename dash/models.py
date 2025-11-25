from extensions import db
from datetime import datetime

# ==================== MANY-TO-MANY TABLES ======================

compulsarysubject_class = db.Table(
    "compulsarysubject_class",
    db.Column("classroom_id", db.Integer, db.ForeignKey("classroom.id"), primary_key=True),
    db.Column("subject_id", db.Integer, db.ForeignKey("compulsary_subject.id"), primary_key=True),
)


teacherschoolrecord_classroom = db.Table(
    "teacherschoolrecord_classroom",
    db.Column("classroom_id", db.Integer, db.ForeignKey("classroom.id"), primary_key=True),
    db.Column("teacherschoolrecord_id", db.Integer, db.ForeignKey("teacher_school_record.id"), primary_key=True),
)

# ==================== SUBJECT MODELS ========================

class CompulsarySubject(db.Model):
    __tablename__ = "compulsary_subject"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), nullable=False, unique=True)
    subject_code = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self,subject_name,subject_code) -> None:
        self.subject_name = subject_name
        self.subject_code = subject_code
        


class OptionalSubject(db.Model):
    __tablename__ = "optional_subject"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), nullable=False, unique=True)
    subject_code = db.Column(db.String(50), nullable=False, unique=True)

    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"))

    def __init__(self,subject_name,subject_code,classroom_id) -> None:
        self.subject_name = subject_name
        self.subject_code = subject_code
        self.classroom_id = classroom_id
        



    # ==================== CLASSROOM =============================

class Classroom(db.Model):
    __tablename__ = "classroom"

    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(50), nullable=False, unique=True)

    # many-to-many
    compulsary_subjects = db.relationship(
        "CompulsarySubject",
        secondary=compulsarysubject_class,
        backref="classrooms",
        lazy="joined"
    )

    # one-to-many
    optional_subjects = db.relationship("OptionalSubject", backref="classroom", lazy="joined")

    # many-to-many with teacher school record
    teacherschoolrecords = db.relationship(
        "TeacherSchoolRecord",
        secondary="teacherschoolrecord_classroom",
        overlaps="classrooms",
        lazy="joined")

    # one-to-many: StudentSchoolRecord.classroom_id must exist (added in auth.models)
    student_school_record = db.relationship(
        "StudentSchoolRecord", 
        backref="classroom", 
        lazy="joined")

    # class_assignments = db.relationship("ClassAssignment", backref="classroom", lazy="joined")

    def __init__(self, classroom_name) -> None:
        self.classroom_name = classroom_name
        