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
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: Compulsary-Subject-Name = {self.subject_name},Compulsary-Subject-Name = {self.subject_code}"

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
        lazy="joined",
        uselist=True
        )

    def __init__(self, classroom_name) -> None:
        self.classroom_name = classroom_name


# ==================== STUDENT ATTENDANCE MODEL ============================= 
class StudentAttendance(db.Model):
    __tablename__ = "student_attendance"

    id = db.Column(db.Integer, primary_key=True)

    # Updated to match routes (Present / Absent)
    status = db.Column(db.String(20), nullable=False)

    # Needed because your endpoints use attendance_date=today
    attendance_date = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Keep FK unchanged
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey('student_school_record.id'),
        nullable=False
    )

    def __init__(self, status, attendance_date, student_school_record_id):
        self.status = status
        self.attendance_date = attendance_date
        self.student_school_record_id = student_school_record_id

   

# ==================== STUDENT GRADE MODEL ============================= 
class StudentGrade(db.Model):
    __tablename__ = "student_grade"
    id = db.Column(db.Integer,primary_key=True) 
    exam_name = db.Column(db.String(50),nullable=False)
    exam_code = db.Column(db.String(50),nullable=False)
    exam_subject_name = db.Column(db.String(50),nullable=False)
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
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: Student-Score = {self.student_score}, Student-FK = {self.student_school_record_id}"
    
    def __init__(self,exam_name,exam_code,exam_subject_name,student_score,student_grade,student_school_record_id) -> None:
        self.exam_name = exam_name
        self.exam_code = exam_code
        self.exam_subject_name = exam_subject_name
        self.student_score = student_score
        self.student_grade = student_grade
        self.student_school_record_id = student_school_record_id
    
  


# ==================== STUDENT ASSIGNMENT MODEL ============================= 
class ClassAssignment(db.Model):
    __tablename__ = "class_assignment"

    id = db.Column(db.Integer,primary_key=True)
    created_by_first_name = db.Column(db.String(50),nullable=False,server_default="Placeholder First Name") 
    created_by_last_name = db.Column(db.String(50),nullable=False,server_default="Placeholder Last Name")  
    assignment_name = db.Column(db.String(50),nullable=False)
    assignment_subject_Name = db.Column(db.String(50),nullable=False)
    assignment_subject_code = db.Column(db.String(50),nullable=False)
    due_date = db.Column(db.DateTime,default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    # relationships
    # one : many
    assignment_file_uploads = db.relationship(
        "AssignmentFileUpload",
        backref="class_assignment",
        uselist=True,
        lazy="joined"
        )
    
    assignment_submisssion_file_uploads = db.relationship(
        "StudentAssignmentSubmission",
        backref="class_assignment",
        uselist=True,
        lazy="joined"
        )
    
    # fk
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classroom.id'),
        )
    
    def __init__(self,assignment_name,assignment_subject_Name,assignment_subject_code,classroom_id) -> None:
        self.assignment_name = assignment_name
        self.assignment_subject_Name = assignment_subject_Name
        self.assignment_subject_code = assignment_subject_code
        self.classroom_id= classroom_id
    


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
    
    def __init__(self,original_name,filename,filepath,class_assignment_id) -> None:
        self.original_name = original_name
        self.filename = filename
        self.filepath = filepath
        self.class_assignment_id = class_assignment_id
        


# ==================== STUDENT ASSIGNMENT SUBMISSION MODEL ============================= 
class StudentAssignmentSubmission(db.Model):
    __tablename__ = "student_assignment_submission"

    id = db.Column(db.Integer,primary_key=True) 
    submitted_by_first_name = db.Column(db.String(50),nullable=False,server_default="Placeholder First Name") 
    submitted_by_last_name = db.Column(db.String(50),nullable=False,server_default="Placeholder Last Name") 
    assignment_name = db.Column(db.String(50),nullable=False)
    assignment_subject_Name = db.Column(db.String(50),nullable=False)
    assignment_subject_code = db.Column(db.String(50),nullable=False)
    student_score = db.Column(db.Integer,nullable=False,default=0) 
    student_grade = db.Column(db.String(5),nullable=False,default="No Grade") 
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)


    # relationships
    
    # one : many 
    assignment_submisssion_file_uploads = db.relationship(
        "AssignmentSubmisssionFileUpload",
        backref="student_assignment_submission",
        uselist=True,
        lazy="joined"
        )
    
    # fk
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey("student_school_record.id"),
        nullable=False
    )

    class_assignment_id = db.Column(
        db.Integer,
        db.ForeignKey("class_assignment.id"),
        nullable=False
    )
    
    def __init__(
            self,assignment_name,
            assignment_subject_Name,
            assignment_subject_code,
            student_school_record_id,
            class_assignment_id,
            submitted_by_first_name="Placeholder First Name",
            submitted_by_last_name="Placeholder Last Name",
            student_score=0,
            student_grade="No Grade") -> None:
        self.assignment_name = assignment_name
        self.assignment_subject_Name = assignment_subject_Name
        self.assignment_subject_code = assignment_subject_code
        self.student_school_record_id = student_school_record_id
        self.class_assignment_id = class_assignment_id
        self.submitted_by_first_name = submitted_by_first_name
        self.submitted_by_last_name = submitted_by_last_name
        self.student_score = student_score
        self.student_grade = student_grade
    


# ==================== STUDENT ASSIGNMENT SUBMISSION MODEL ============================= 

class AssignmentSubmisssionFileUpload(db.Model):
    __tablename__ = "assignment_submisssion_file_upload"
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    original_name = db.Column(db.String(500),nullable=False) 
    filename = db.Column(db.String(500),nullable=False) 
    filepath = db.Column(db.String(500),nullable=False) 
    # fk
    student_assignment_submission_id = db.Column(
        db.Integer,
        db.ForeignKey('student_assignment_submission.id'),
        nullable=False
        )
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.filename}"
    
    def __init__(self,original_name,filename,filepath,student_assignment_submission_id) -> None:
        self.original_name = original_name
        self.filename = filename
        self.filepath = filepath
        self.student_assignment_submission_id = student_assignment_submission_id


                