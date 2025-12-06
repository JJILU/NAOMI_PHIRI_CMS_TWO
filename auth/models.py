from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from dash.models import teacherschoolrecord_compulsarysubject,teacherschoolrecord_optionalsubject
# from uuid import uuid4


# ========================= School Records Database ==========================

class TeacherSchoolRecord(db.Model):
    __tablename__ = "teacher_school_record"
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False) 
    last_name = db.Column(db.String(50),nullable=False) 
    card_id = db.Column(db.String(50),nullable=False) 
    
      
    # one : one relationship
    teacher = db.relationship(
        "Teacher",
        backref="teacherschoolrecord",
        uselist=False,
        lazy="joined"
        )

    # many : many relationship
    compulsarysubject = db.relationship(
        "CompulsarySubject",
        secondary=teacherschoolrecord_compulsarysubject,
        overlaps="teacherschoolrecords",
        lazy="joined"
        )
    
    optionalsubject = db.relationship(
        "OptionalSubject",
        secondary=teacherschoolrecord_optionalsubject,
        overlaps="teacherschoolrecords",
        lazy="joined"
        )
    
    # one : one relationship
    teacher_avator = db.relationship(
        "AvatorFileUpload",
         backref="teacher_school_record",
         uselist=False,
         lazy="joined"
        )
    


    def __init__(self,first_name,last_name,card_id):
        self.first_name = first_name
        self.last_name = last_name
        self.card_id = card_id

    # check if teacher id is in school records, before creating one
    @classmethod
    def get_teacher_by_card_id(cls,card_id):
        return TeacherSchoolRecord.query.filter_by(card_id=card_id).first()    


class StudentSchoolRecord(db.Model):
    __tablename__ = "student_school_record"
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    first_name = db.Column(db.String(50),nullable=False) 
    last_name = db.Column(db.String(50),nullable=False) 
    card_id = db.Column(db.String(50),nullable=False) 
    is_admin = db.Column(db.Boolean,default=False)
    
    # one : one relationship
    student = db.relationship(
        "Student",
        backref="student",
        uselist=False,
        lazy="joined"
        )
    admin = db.relationship(
        "Admin",
        backref="admin",
        uselist=False,
        lazy="joined"
        )
    
    # one : many relationship
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classroom.id'),
        nullable=False
    )

    # one : many relationship
    student_grades = db.relationship(
        "StudentGrade",
        backref="student_record",
        uselist=True,
        lazy="joined"
        )
    
     # one : many relationship
    student_attendances = db.relationship(
        "StudentAttendance",
        backref="student_record",
        uselist=True,
        lazy="joined"
        )

    # one : one relationship
    student_avator = db.relationship(
        "AvatorFileUpload",
         backref="student_school_record",
         uselist=False,
         lazy="joined"
        )
    
    # one : many
    student_assignment_submission = db.relationship(
        "StudentAssignmentSubmission",
        backref="student_school_record",
        uselist=True,
        lazy="joined"
        )
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:School-ID = {self.card_id},First-Name = {self.first_name}, Is_Admin = {self.is_admin}"

    def __init__(self,first_name,last_name,card_id,is_admin,classroom_id):
        self.first_name = first_name
        self.last_name = last_name
        self.card_id = card_id
        self.is_admin = is_admin
        self.classroom_id = classroom_id

        # check if teacher id is in school records, before creating one
    @classmethod
    def get_student_by_card_id(cls,card_id):
        return StudentSchoolRecord.query.filter_by(card_id=card_id).first()     


# ======================= Avator Model ======================
class AvatorFileUpload(db.Model):
    __tablename__ = "avator_fileupload"
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    original_name = db.Column(db.String(500),nullable=False) 
    filename = db.Column(db.String(500),nullable=False) 
    filepath = db.Column(db.String(500),nullable=False) 



    # fk
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey('student_school_record.id'), nullable=False
        )
    
    teacher_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey('teacher_school_record.id'), 
        nullable=False,
        unique=True
        )
    
    def __init__(self,original_name,filename,filepath):
        self.original_name = original_name
        self.filename = filename
        self.filepath = filepath

        
# ========================= Classroom Management Users ==========================

# --------------- 1: Teacher ClassFlow Model --------------------

class Teacher(db.Model,UserMixin):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    user_card_id = db.Column(db.String(50),nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    
    # fk
    teacher_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_school_record.id"),
        unique=True,
        nullable=False
        )
  
    

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: teacher card id {self.user_card_id}>"
    
    def __init__(self, user_card_id, password,role,teacher_school_record_id) -> None:
        self.user_card_id = user_card_id
        self.hashed_password = self.set_hashed_password(password)
        self.role = role
        self.teacher_school_record_id = teacher_school_record_id

    # used to load current user
    def get_id(self):
        return f"Teacher:{self.id}"     

    # hash password at registration
    def set_hashed_password(self,password):
        return generate_password_hash(password)
    
    # compare hashed password to password submitted at login
    def check_hashed_password(self,password):
        return check_password_hash(self.hashed_password,password)
    
    # check if teacher already has account, before creating one
    @classmethod
    def get_teacher_card_id(cls,user_card_id):
        return Teacher.query.filter_by(user_card_id=user_card_id).first()
    
    # save new teacher account to table
    def save_teacher(self):
        db.session.add(self)
        db.session.commit()

    # delete new teacher account to table
    def delete_teacher(self):
      db.session.delete(self)
      db.session.commit()

      



# --------------- 2: Admin ClassFlow Model --------------------

class Admin(db.Model,UserMixin):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    user_card_id = db.Column(db.String,nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey("student_school_record.id"),
        unique=True,
        nullable=False
        )


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: admin card id {self.user_card_id}>"
    
    def __init__(self, user_card_id, password,role,student_school_record_id) -> None:
        self.user_card_id = user_card_id
        self.hashed_password= self.set_hashed_password(password)
        self.role = role
        self.student_school_record_id = student_school_record_id

    # used to load current user
    def get_id(self):
        return f"Admin:{self.id}"    

    # hash password at registration
    def set_hashed_password(self,password):
        return generate_password_hash(password)
    
    # compare hashed password to password submitted at login
    def check_hashed_password(self,password):
        return check_password_hash(self.hashed_password,password)
    
    # check if admin already has account, before creating one
    @classmethod
    def get_user_card_id(cls,user_card_id):
        return Admin.query.filter_by(user_card_id=user_card_id).first()
    
    # save new admin account to table
    def save_admin(self):
        db.session.add(self)
        db.session.commit()

    # delete new admin account to table
    def delete_admin(self):
      db.session.delete(self)
      db.session.commit()

       


# --------------- 3: Student Class Room Management Model --------------------

class Student(db.Model,UserMixin):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    user_card_id = db.Column(db.String,nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    # fk
    student_school_record_id = db.Column(
        db.Integer,
        db.ForeignKey("student_school_record.id"),
        unique=True,
        nullable=False
        )
    


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: student card id {self.user_card_id}>, student fk {self.student_school_record_id}"
    
    def __init__(self, user_card_id, password,role,student_school_record_id) -> None:
        self.user_card_id = user_card_id
        self.hashed_password = self.set_hashed_password(password)
        self.role = role
        self.student_school_record_id = student_school_record_id

    # used to load current user
    def get_id(self):
        return f"Student:{self.id}"    


    # hash password at registration
    def set_hashed_password(self,password):
        return generate_password_hash(password)
    
    # compare hashed password to password submitted at login
    def check_hashed_password(self,password):
        return check_password_hash(self.hashed_password,password)
    
    # check if  already has account, before creating one
    @classmethod
    def get_user_card_id(cls,user_card_id):
        return Student.query.filter_by(user_card_id=user_card_id).first()
    
    # save new student account to table
    def save_student(self):
        db.session.add(self)
        db.session.commit()

    # delete student account to table
    def delete_student(self):
      db.session.delete(self)
      db.session.commit() 



          


   



       
