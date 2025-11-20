from extensions import db 

# class StudentSchoolRecord(db.Model):
#     # id = db.Column(db.String(255),primary_key=True, default=str(uuid4()))
#     id = db.Column(db.Integer,primary_key=True)   
#     first_name = db.Column(db.String(50),nullable=False) 
#     last_name = db.Column(db.String(50),nullable=False) 
#     card_id = db.Column(db.String(50),nullable=False) 
#     is_admin = db.Column(db.Boolean,default=False)
#     # filename = db.Column(db.String(500),nullable=False) 
#     # filepath = db.Column(db.String(500),nullable=False) 

#     school_id = db.Column(db.Integer,db.ForeignKey("teacher.id"),unique=True,nullable=False)



#     def __init__(self,first_name,last_name,card_id):
#         self.first_name = first_name # type: ignore
#         self.last_name = last_name
#         self.card_id = card_id

#         # check if teacher id is in school records, before creating one
#     @classmethod
#     def get_student_by_card_id(cls,card_id):
#         return StudentSchoolRecord.query.filter_by(card_id=card_id).first()  



# class ProfileFileUpload(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     original_file_name = db.Column(db.String(255),nullable=False)    
#     filepath = db.Column(db.String(255),nullable=False)    
#     filename = db.Column(db.String(255),nullable=False) 



class ClassRoom(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False, unique=True)

    assignments = db.relationship("Assignment",backref="classroom", uselist=True)


class Assignment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(100),nullable=False)

    classroom_id = db.Column(db.Integer,db.ForeignKey("classroom.id"))

    file_uploads = db.relationship("AssignmentFileUpload", backref="assignment", uselist=True)


class AssignmentFileUpload(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    original_file_name = db.Column(db.String(255),nullable=False)    
    filepath = db.Column(db.String(255),nullable=False)    
    filename = db.Column(db.String(255),nullable=False)    

    assignment_id = db.Column(db.Integer,db.ForeignKey("assignment.id"))

