from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from dash.models import StudentAttendance
# from uuid import uuid4


# ========================= School Records Database ==========================

class TeacherSchoolRecord(db.Model):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False) 
    last_name = db.Column(db.String(50),nullable=False) 
    card_id = db.Column(db.String(50),nullable=False) 
    # filename = db.Column(db.String(500),nullable=False) 
    # filepath = db.Column(db.String(500),nullable=False) 

    teacher_id = db.Column(db.Integer,db.ForeignKey("teacher.id"),unique=True,nullable=False)

    def __init__(self,first_name,last_name,card_id):
        self.first_name = first_name
        self.last_name = last_name
        self.card_id = card_id

    # check if teacher id is in school records, before creating one
    @classmethod
    def get_teacher_by_card_id(cls,card_id):
        return TeacherSchoolRecord.query.filter_by(card_id=card_id).first()    


class StudentSchoolRecord(db.Model):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)   
    first_name = db.Column(db.String(50),nullable=False) 
    last_name = db.Column(db.String(50),nullable=False) 
    card_id = db.Column(db.String(50),nullable=False) 
    is_admin = db.Column(db.Boolean,default=False)
    # filename = db.Column(db.String(500),nullable=False) 
    # filepath = db.Column(db.String(500),nullable=False) 

    student_school_id = db.Column(db.Integer,db.ForeignKey("student.id"),unique=True,nullable=False)
    admin_school_id = db.Column(db.Integer,db.ForeignKey("admin.id"),unique=True,nullable=False)



    def __init__(self,first_name,last_name,card_id, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.card_id = card_id
        self.is_admin =  is_admin

        # check if teacher id is in school records, before creating one
    @classmethod
    def get_student_by_card_id(cls,card_id):
        return StudentSchoolRecord.query.filter_by(card_id=card_id).first()     



        
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
    
    # one:one relationship
    teacher_school_record = db.relationship("TeacherSchoolRecord",backref="teacher",uselist=False,lazy="joined")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: teacher card id {self.user_card_id}>"
    
    def __init__(self, user_card_id, password,role) -> None:
        self.user_card_id = user_card_id
        self.hashed_password = self.set_hashed_password(password)
        self.role = role

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

    # one:one relationship
    admin_school_record = db.relationship("StudentSchoolRecord",backref="admin",uselist=False,lazy="joined")
    # one:many
    admin_attendance = db.relationship("StudentAttendance",backref="admin",uselist=True,lazy="joined")


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: admin card id {self.user_card_id}>"
    
    def __init__(self, user_card_id, password,role) -> None:
        self.user_card_id = user_card_id
        self.hashed_password= self.set_hashed_password(password)
        self.role = role

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

       


# --------------- 3: Student ClassFlow Model --------------------

class Student(db.Model,UserMixin):
    # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
    id = db.Column(db.Integer,primary_key=True)
    user_card_id = db.Column(db.String,nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)

    # one:one relationship
    student_school_record = db.relationship("StudentSchoolRecord",backref="student",uselist=False,lazy="joined")
    # one:many relationship
    student_attendance = db.relationship("StudentAttendance",backref="student",uselist=True,lazy="joined")


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: student card id {self.user_card_id}>"
    
    def __init__(self, user_card_id, password,role) -> None:
        self.user_card_id = user_card_id
        self.hashed_password = self.set_hashed_password(password)
        self.role = role

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



          


   



       
