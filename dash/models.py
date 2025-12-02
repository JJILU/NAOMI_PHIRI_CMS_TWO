from extensions import db
from datetime import datetime

# ==================== MANY-TO-MANY TABLES ======================

compulsarysubject_class = db.Table(
    "compulsarysubject_class",
    db.Column("classroom_id", db.Integer, db.ForeignKey("classroom.id"), primary_key=True),
    db.Column("subject_id", db.Integer, db.ForeignKey("compulsary_subject.id"), primary_key=True),
)


teacherschoolrecord_compulsarysubject = db.Table(
    "teacherschoolrecord_compulsarysubject",
    db.Column("compulsary_subject_id", db.Integer, db.ForeignKey("compulsary_subject.id"), primary_key=True),
    db.Column("teacherschoolrecord_id", db.Integer, db.ForeignKey("teacher_school_record.id"), primary_key=True),
)


teacherschoolrecord_optionalsubject = db.Table(
    "teacherschoolrecord_optionalsubject",
    db.Column("optional_subject_id", db.Integer, db.ForeignKey("optional_subject.id"), primary_key=True),
    db.Column("teacherschoolrecord_id", db.Integer, db.ForeignKey("teacher_school_record.id"), primary_key=True),
)
# ==================== SUBJECT MODELS ========================

class CompulsarySubject(db.Model):
    __tablename__ = "compulsary_subject"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), nullable=False, unique=True)
    subject_code = db.Column(db.String(50), nullable=False, unique=True)

    teacherschoolrecords = db.relationship(
        "TeacherSchoolRecord",
        secondary="teacherschoolrecord_compulsarysubject",
        overlaps="compulsarysubject",
        lazy="joined"
        )

    def __init__(self,subject_name,subject_code) -> None:
        self.subject_name = subject_name
        self.subject_code = subject_code
        


class OptionalSubject(db.Model):
    __tablename__ = "optional_subject"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), nullable=False, unique=True)
    subject_code = db.Column(db.String(50), nullable=False, unique=True)

    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"))

    teacherschoolrecords = db.relationship(
        "TeacherSchoolRecord",
        secondary="teacherschoolrecord_optionalsubject",
        overlaps="optionalsubject",
        lazy="joined"
        )

    def __init__(self,subject_name,subject_code,classroom_id) -> None:
        self.subject_name = subject_name
        self.subject_code = subject_code
        self.classroom_id = classroom_id
        



# ==================== CLASSROOM MODEL ============================= 

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
    optional_subjects = db.relationship(
        "OptionalSubject", 
        backref="classroom", 
        lazy="joined"
        )

  
    # one-to-many: StudentSchoolRecord.classroom_id must exist (added in auth.models)
    student_school_record = db.relationship(
        "StudentSchoolRecord", 
        backref="classroom", 
        lazy="joined")
    
    # one-to-many: ClassAssignment.classroom_id must exist (added in dash.models)
    class_assignments = db.relationship(
        "ClassAssignment", 
        backref="classroom", 
        lazy="joined"
        )

    def __init__(self, classroom_name) -> None:
        self.classroom_name = classroom_name


# ==================== STUDENT ATTENDANCE MODEL ============================= 
class StudentAttendance(db.Model):
    __tablename__ = "student_attendance"

    id = db.Column(db.Integer,primary_key=True) 
    is_present = db.Column(db.Boolean,nullable=False,default=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    
    # fk
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey('student_school_record.id'),
        nullable=False
        )
    
    def __init__(self, is_present,student_school_record_id):
        self.is_present = is_present
        self.student_school_record_id = student_school_record_id
         
    
   

# ==================== STUDENT GRADE MODEL ============================= 
class StudentGrade(db.Model):
    __tablename__ = "student_grade"
    id = db.Column(db.Integer,primary_key=True) 
    exam_name = db.Column(db.String(50),nullable=False)
    exam_code = db.Column(db.String(50),nullable=False)
    exam_subject_Name = db.Column(db.String(50),nullable=False)
    student_score = db.Column(db.Integer,nullable=False) 
    student_grade = db.Column(db.String(5),nullable=False) 
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    # fk
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey('student_school_record.id'),
        nullable=False
        )
    
  


# ==================== STUDENT ASSIGNMENT MODEL ============================= 
class ClassAssignment(db.Model):
    __tablename__ = "class_assignment"

    id = db.Column(db.Integer,primary_key=True) 
    assignment_name = db.Column(db.String(50),nullable=False)
    assignment_subject_Name = db.Column(db.String(50),nullable=False)
    assignment_subject_code = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    # relationships
    
    assignment_file_uploads = db.relationship(
        "AssignmentFileUpload",
        backref="class_assignment",
        uselist=True,
        lazy="joined"
        )
    
    # fk
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classroom.id'),
        )
    


# ==================== STUDENT ASSIGNMENT MODEL ============================= 

class AssignmentFileUpload(db.Model):
    __tablename__ = "assignment_fileupload"
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    original_name = db.Column(db.String(500),nullable=False) 
    filename = db.Column(db.String(500),nullable=False) 
    filepath = db.Column(db.String(500),nullable=False) 
    # fk
    class_assignment_id = db.Column(
        db.Integer,
        db.ForeignKey('class_assignment.id'),
        nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.filename}"


        