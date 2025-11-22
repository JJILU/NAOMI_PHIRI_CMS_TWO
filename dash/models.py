from extensions import db
from auth.models import Teacher,Admin,Student,TeacherSchoolRecord,StudentSchoolRecord
from datetime import datetime

# =========== Dashboard End-Points ===================

compulsarysubject_class = db.Table(
    "compulsarysubject_class",
    db.Column(db.Integer,db.ForeignKey('compulsarysubject.id')),
    db.Column(db.Integer,db.ForeignKey('classroom.id')),
)

class CompulsarySubject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(50),nullable=False,unique=True) 
    subject_code = db.Column(db.String(50),nullable=False,unique=True) 




class OptionalSubject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(50),nullable=False,unique=True) 
    subject_code = db.Column(db.String(50),nullable=False,unique=True) 

    # fk
    classroom_id = db.Column(db.Integer,db.ForeignKey('classroom.id'))
    classroom = db.relationship("Classroom", backref="optional_subjects")


teacher_school_record_class = db.Table(
    "teacher_school_record_class",
    db.Column(db.Integer,db.ForeignKey('teacherschoolrecord.id')),
    db.Column(db.Integer,db.ForeignKey('classroom.id')),
)


class Classroom(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    classroom_name = db.Column(db.String(50),nullable=False,unique=True) 
    # relationships
    compulsary_subjects = db.relationship("CompulsarySubject",secondary=compulsarysubject_class,backref="classrooms",lazy="joined")
    optional_subjects = db.relationship("OptionalSubject",backref="classroom",uselist=True,lazy="joined")
    teacher_school_record = db.relationship("TeacherSchoolRecord",secondary=teacher_school_record_class,backref="classrooms",lazy="joined")
    student_school_record = db.relationship("StudentSchoolRecord",backref="classroom",uselist=True,lazy="joined")
    assignments = db.relationship("ClassAssignments",backref="classroom",uselist=True,lazy="joined")
    # teachers = db.relationship("Teacher",secondary=teacher_class,backref="classroom",lazy="joined")
    # admin = db.relationship("Admin",backref="classroom",uselist=True,lazy="joined")
    # students = db.relationship("Student",backref="classroom",uselist=True,lazy="joined")


class StudentAttendance(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    is_present = db.Column(db.Boolean,nullable=False,default=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    # fk
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    # relationships
    student = db.relationship("Student",backref="student_attendances",lazy="joined")


class StudentGrade(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    exam_name = db.Column(db.String(50),nullable=False)
    exam_code = db.Column(db.String(50),nullable=False)
    exam_subject_Name = db.Column(db.String(50),nullable=False)
    student_score = db.Column(db.Integer,nullable=False) 
    student_grade = db.Column(db.String(5),nullable=False) 
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    # fk
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    # relationships
    student = db.relationship("Student",backref="student_grade",uselist=False,lazy="joined")


class ClassAssignment(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    assignment_name = db.Column(db.String(50),nullable=False)
    assignment_code = db.Column(db.String(50),nullable=False)
    assignment_subject_Name = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    # fk
    classroom_id = db.Column(db.Integer,db.ForeignKey('classroom.id'))
    # relationships
    classroom = db.relationship("Classroom",backref="class_assignments",lazy="joined")
    assignment_file_uploads = db.relationship("AssignmentFileUpload",backref="class_assignment",uselist=True,lazy="joined")



class AssignmentFileUpload(db.Model):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    filename = db.Column(db.String(500),nullable=False) 
    filepath = db.Column(db.String(500),nullable=False) 
    # fk
    classassingment_id = db.Column(db.Integer,db.ForeignKey('classassignment.id'))