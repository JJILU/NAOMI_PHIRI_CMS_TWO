from auth.models import TeacherSchoolRecord
from dash.models import CompulsarySubject,OptionalSubject
from app import create_app
from extensions import db
from random import choice


app = create_app()

# get subjects
def get_all_compulsary_subjects() -> list:
    all_compulsary_subjects = CompulsarySubject.query.all()
    return all_compulsary_subjects

def get_all_options_subjects() -> list:
    all_optional_subjects = OptionalSubject.query.all()
    return all_optional_subjects

def get_all_teachers() -> list:
    all_teachers = TeacherSchoolRecord.query.all()
    return all_teachers

with app.app_context():
  try:
    for cs in get_all_compulsary_subjects():
      teacher = choice(get_all_teachers())
      cs.teacherschoolrecords.append(teacher)


    for os in get_all_options_subjects():
        teacher = choice(get_all_teachers())
        os.teacherschoolrecords.append(teacher)  

    db.session.commit()    
    print("successfully associated teacher teachers to subjects")  
  except Exception as e:
     db.session.rollback()
     print(f"Falied to associated teacher teachers to subjects: {str(e)}")  

     



  teacher = TeacherSchoolRecord.query.get(9)
  if teacher:
    print(teacher.compulsarysubject)
    print(teacher.optionalsubject)
