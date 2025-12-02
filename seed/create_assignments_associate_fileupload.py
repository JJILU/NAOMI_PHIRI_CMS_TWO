from dash.models import ClassAssignment, AssignmentFileUpload, Classroom
from app import create_app
from extensions import db, faker
from random import choices

app = create_app()

def get_all_classrooms():
    return Classroom.query.all()

with app.app_context():

    # for classroom in get_all_classrooms():

    #     cs_list = classroom.compulsary_subjects
    #     op_list = classroom.optional_subjects

    #     if not cs_list or not op_list:
    #         print("Classroom has no subjects. Skipping...")
    #         continue

    #     # pick random compulsory + optional
    #     com_subject = choices(cs_list, k=1)[0]
    #     optional = choices(op_list, k=1)[0]

    #     assignment_subject = choices([com_subject, optional], k=1)[0]

    #     try:
    #         new_assignment = ClassAssignment(
    #             assignment_name=faker.sentence(nb_words=3),  # FIXED
    #             assignment_subject_Name=assignment_subject.subject_name,  # FIXED
    #             assignment_subject_code=assignment_subject.subject_code,
    #             classroom_id=classroom.id
    #         )

    #         db.session.add(new_assignment)      # MISSING
    #         db.session.commit()                 # MISSING


            

    #         print("Successfully created assignments with file uploads")

    #     except Exception as e:
    #         db.session.rollback()
    #         print(f"Failed to create assignment: {str(e)}")


    # get all assignment and attach file uploads
    all_class_assignmnts = ClassAssignment.query.all()

    for assignment in all_class_assignmnts:
        try:
            new_file = AssignmentFileUpload(
            original_name=faker.file_name(),
            filename=faker.file_name(),
            filepath=faker.file_path(depth=3, category="image")
            )
            new_file.class_assignment_id = assignment.id
            db.session.add(new_file)

            db.session.commit()
            print(f"successfully attach files to assignments")  
        except Exception as e:
            db.session.rollback()
            print(f"failed to attach file to assignments {str(e)}")     
