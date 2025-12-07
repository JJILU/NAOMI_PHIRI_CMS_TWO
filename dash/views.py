from flask import render_template, redirect, url_for, request, abort, jsonify, current_app,send_from_directory
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import desc, asc
from extensions import db,faker
from random import choice
import os
from werkzeug.utils import secure_filename


from . import dash_bp


@dash_bp.before_request
def require_login():
    # Allow static files
    if request.endpoint and request.endpoint.startswith("static"):
        return
    # Allow browser favicon request
    if request.path == "/favicon.ico":
        return

    # Block ALL views unless user logged in
    if not current_user.is_authenticated: # type: ignore
        return redirect(url_for("auth.login"))

    # Example: allow certain views without restriction
    # (use real endpoint names)
    # if request.endpoint in ["dash_bp.index"]:
    #     return


def role_required(*roles):
    """
    Usage:
        @role_required("Admin", "Teacher")
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Must be logged in
            if not current_user.is_authenticated: # type: ignore
                return redirect(url_for("auth.login"))

            # User logged in but wrong role → Forbidden
            if current_user.role not in roles: # type: ignore
                return abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator


chat_bot_responses = {
    "greeting":["😊 Hello, what question do have","🖐 Hi what how can i help","Hi 😎","🤗Hi there"],
    "attendance":"",
    "assignments":"",
    "assignments":"",
    "grading":"",
    "update profile":"",
}


@dash_bp.route("/")
@role_required("teacher", "admin")
def index():
    return render_template("index.html")


# ------------------ Admin Management End-Points ------------------------
@dash_bp.route("/create_admin", methods=["GET", "POST"])
@role_required("teacher")
def create_admin():

    return render_template("admin_management/create_admin.html")


@dash_bp.route("/view_admins", methods=["GET", "POST"])
@role_required("teacher")
def view_admins():
    return render_template("admin_management/view_admins.html")


@dash_bp.route("/view_one_admin/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def view_one_admin(id):
    return render_template("admin_management/view_one_admin.html")


@dash_bp.route("/update_admin/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def update_admin(id):
    return render_template("admin_management/update_admin.html")


@dash_bp.route("/delete_admin/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def delete_admin(id):
    return render_template("student_management/delete_admin.html")


# ------------------ Student Management End-Points ------------------------
@dash_bp.route("/create_student_school_record", methods=["GET", "POST"])
@role_required("teacher", "admin")
def create_student_school_record():
    from auth.models import StudentSchoolRecord, AvatorFileUpload
    from dash.models import Classroom
    classrooms = Classroom.query.all()
    error = None

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        classroom_id = request.form.get("classroom_id")
        is_admin = True if request.form.get("is_admin") else False
        avatar_file = request.files.get("avatar_file")

        if not first_name or not last_name or not classroom_id:
            error = "All fields are required."
            return render_template(
                "student_management/create_student_school_record.html",
                classrooms=classrooms,
                error=error
            )

        # --- GENERATE UNIQUE STUDENT ID ---
        while True:
            generated_id = faker.generate_student_id()
            exists = StudentSchoolRecord.query.filter_by(card_id=generated_id).first()
            if not exists:
                break

        # --- SAVE STUDENT RECORD ---
        new_student = StudentSchoolRecord(
            first_name=first_name,
            last_name=last_name,
            card_id=generated_id,
            is_admin=is_admin,
            classroom_id=classroom_id
        )
        db.session.add(new_student)
        db.session.commit()

        # --- SAVE AVATAR FILE ---
        if avatar_file and avatar_file.filename != "":
            filename = secure_filename(avatar_file.filename) # type: ignore
            upload_path = os.path.join(current_app.config["PROFILE_PHOTO_UPLOAD"], filename)
            avatar_file.save(upload_path)

            avatar_record = AvatorFileUpload(
                original_name=avatar_file.filename,
                filename=filename,
                filepath=upload_path,
                student_school_record_id=new_student.id,
            )
            db.session.add(avatar_record)
            db.session.commit()

        return redirect(url_for("dash.view_students"))

    return render_template(
        "student_management/create_student_school_record.html",
        classrooms=classrooms,
        error=error
    )

# -------------------------
# VIEW STUDENTS
# -------------------------
@dash_bp.route("/view_students")
@role_required("teacher", "admin")
def view_students():
    from auth.models import StudentSchoolRecord
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    students_paginated = StudentSchoolRecord.query.order_by(
        StudentSchoolRecord.id.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "student_management/view_students_records.html",
        students=students_paginated.items,
        pagination=students_paginated,
        per_page=per_page
    )

# -------------------------
# VIEW ONE STUDENT
# -------------------------
@dash_bp.route("/view_one_student/<int:id>")
@role_required("teacher", "admin")
def view_one_student(id):
    from auth.models import StudentSchoolRecord
    student = StudentSchoolRecord.query.get_or_404(id)
    return render_template("student_management/view_one_student_detail.html", student=student)

# -------------------------
# UPDATE STUDENT
# -------------------------
@dash_bp.route("/update_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def update_student(id):
    from auth.models import StudentSchoolRecord, AvatorFileUpload
    from dash.models import Classroom

    student = StudentSchoolRecord.query.get_or_404(id)
    classrooms = Classroom.query.all()

    if request.method == "POST":
        student.first_name = request.form.get("first_name")
        student.last_name = request.form.get("last_name")
        student.classroom_id = request.form.get("classroom_id")
        # Handle admin checkbox
        student.is_admin = True if request.form.get("is_admin") else False

        avatar_file = request.files.get("avatar_file")
        db.session.commit()

        # --- Update avatar if new file uploaded ---
        if avatar_file and avatar_file.filename != "":
            filename = secure_filename(avatar_file.filename) # type: ignore
            upload_path = os.path.join(current_app.config["PROFILE_PHOTO_UPLOAD"], filename)
            avatar_file.save(upload_path)

            if student.student_avator:
                # Remove old file if exists
                try:
                    os.remove(student.student_avator.filepath)
                except Exception:
                    pass
                student.student_avator.filename = filename
                student.student_avator.filepath = upload_path
                student.student_avator.original_name = avatar_file.filename
            else:
                new_avatar = AvatorFileUpload(
                    original_name=avatar_file.filename,
                    filename=filename,
                    filepath=upload_path,
                    student_school_record_id=student.id,
                    teacher_school_record_id=None
                )
                db.session.add(new_avatar)
            db.session.commit()

        return redirect(url_for("dash.view_students"))

    return render_template(
        "student_management/update_student.html",
        student=student,
        classrooms=classrooms
    )


# -------------------------
# DELETE STUDENT
# -------------------------
@dash_bp.route("/delete_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def delete_student(id):
    from auth.models import StudentSchoolRecord

    student = StudentSchoolRecord.query.get_or_404(id)

    if request.method == "POST":
        # --- Delete avatar file from disk ---
        if student.student_avator:
            avatar_path = student.student_avator.filepath
            if os.path.exists(avatar_path):
                try:
                    os.remove(avatar_path)
                except Exception as e:
                    current_app.logger.warning(f"Failed to delete avatar: {e}")

            db.session.delete(student.student_avator)

        # --- Delete student record ---
        db.session.delete(student)
        db.session.commit()

        return redirect(url_for("dash.view_students"))

    return render_template("student_management/delete_student.html", student=student)


# serve profile avator
@dash_bp.route("/uploads/profile_photo/<filename>")
def uploaded_profile_photo(filename):
    """Serve uploaded profile photo files."""
    return send_from_directory(current_app.config["PROFILE_PHOTO_UPLOAD"], filename)

# ------------------ Student CMS Management ------------------------ 
@dash_bp.route("/create_cms_student", methods=["GET", "POST"])
def create_cms_student():
    from auth.models import StudentSchoolRecord, Student

    available_cards = StudentSchoolRecord.query.order_by(
        StudentSchoolRecord.card_id.asc()).all()

    if request.method == "POST":
        card_id = request.form.get("card_id")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Required checks
        if not password or not confirm_password:
            return render_template(
                "student_management/create_one_student.html",
                error="Password and confirmation are required!",
                card_ids=available_cards
            )

        if password != confirm_password:
            return render_template(
                "student_management/create_one_student.html",
                error="Passwords do not match!",
                card_ids=available_cards
            )

        # Ensure card ID exists in School Records
        school_record = StudentSchoolRecord.query.filter_by(card_id=card_id).first()
        if not school_record:
            return render_template(
                "student_management/create_one_student.html",
                error="Invalid student Card ID selected!",
                card_ids=available_cards
            )

        # Prevent duplicate CMS Accounts
        if Student.get_user_card_id(card_id):
            return render_template(
                "student_management/create_one_student.html",
                error="A CMS account for this student already exists!",
                card_ids=available_cards
            )

        # Create CMS Student
        new_student = Student(
            user_card_id=card_id,
            password=password,
            role="student",
            student_school_record_id=school_record.id
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("dash.view_cms_students"))

    return render_template("student_management/create_one_student.html", card_ids=available_cards)






@dash_bp.route("/view_cms_students")
@role_required("teacher", "admin")
def view_cms_students():
    from auth.models import Student

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    students_paginated = Student.query.order_by(
        Student.id.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "student_management/view_cms_students.html",
        students=students_paginated.items,
        pagination=students_paginated,
        per_page=per_page
    )


@dash_bp.route("/view_one_cms_student/<int:id>")
@role_required("teacher", "admin")
def view_one_cms_student(id):
    from auth.models import Student
    student = Student.query.get_or_404(id)
    return render_template("student_management/view_one_cms_student_detail.html", student=student)

@dash_bp.route("/update_cms_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def update_cms_student(id):
    from auth.models import Student
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        new_password = request.form.get("updated_password")

        if not new_password:
            return render_template(
                "student_management/update_cms_student.html",
                student=student,
                error="Password cannot be empty!"
            )

        student.hashed_password = student.set_hashed_password(new_password)
        db.session.commit()

        return redirect(url_for("dash.view_cms_students"))

    return render_template("student_management/update_cms_student.html", student=student)

@dash_bp.route("/delete_cms_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def delete_cms_student(id):
    from auth.models import Student
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for("dash.view_cms_students"))

    return render_template("student_management/delete_cms_student.html", student=student)





# ------------------ Assignments End-Points ------------------------ [Teacher & Admin]
@dash_bp.route("/create_assignment", methods=["GET", "POST"])
@role_required("teacher")
def create_assignment():

    return render_template("assignment/create_assignment.html")


@dash_bp.route("/view_assignments", methods=["GET", "POST"])
@role_required("teacher", "admin")
def view_assignment():
    return render_template("assignment/view_assignments.html")


@dash_bp.route("/view_one_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin", "student")
def view_one_assignment(id):
    return render_template("student_management/view_one_assignment.html")


@dash_bp.route("/update_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def update_assignment(id):
    return render_template("assignment/update_assignment.html")


@dash_bp.route("/delete_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def delete_assignment(id):
    return render_template("assignment/delete_assignment.html")

# ------------------------------- Assignment Submission [Teacher] ----------------------
@dash_bp.route("/view_assignment_submissions", methods=["GET", "POST"])
@role_required("teacher","admin")
def teacher_view_assignment_submissions():
    return render_template("student_assignment_submission/view_student_assigment_submission.html")


@dash_bp.route("/view_one_assignment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def teacher_view_one_assignment_submission(id):
    return render_template("student_assignment_submission/view_one_student_assigment_submission_detail.html")


@dash_bp.route("/update_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def teacher_update_assigment_submission(id):
    return render_template("student_assignment_submission/update_student_assigment_submission.html")


@dash_bp.route("/delete_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def teacher_delete_assigment_submission(id):
    return render_template("student_assignment_submission/delete_student_assigment_submission.html")


# ------------------ Assignment Submission End-Points ------------------------
@dash_bp.route("/create_assignment_submission", methods=["GET", "POST"])
@role_required("admin", "student")
def create_assignment_submission():

    return render_template("student_assignment_submission/create_student_assigment_submission.html")


@dash_bp.route("/view_assignment_submissions", methods=["GET", "POST"])
@role_required("admin", "student")
def view_assignment_submissions():
    return render_template("student_assignment_submission/view_student_assigment_submission.html")


@dash_bp.route("/view_one_assignment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin", "student")
def view_one_assignment_submission(id):
    return render_template("student_assignment_submission/view_one_student_assigment_submission_detail.html")


@dash_bp.route("/update_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin", "student")
def update_assigment_submission(id):
    return render_template("student_assignment_submission/update_student_assigment_submission.html")


@dash_bp.route("/delete_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin", "student")
def delete_assigment_submission(id):
    return render_template("student_assignment_submission/delete_student_assigment_submission.html")



# ------------------ Grade End-Points ------------------------
# ----------------- List all students to view grades -------------------
@dash_bp.route("/view_grades", methods=["GET"])
@role_required("teacher")
def view_grades():
    from auth.models import StudentSchoolRecord

    students = StudentSchoolRecord.query.all()  # optionally filter by teacher's classes
    return render_template("grades/view_grades.html", students=students)


# ----------------- View all grades for one student -------------------
@dash_bp.route("/view_student_grades/<int:student_id>", methods=["GET"])
@role_required("teacher")
def view_student_grades(student_id):
    from auth.models import StudentSchoolRecord

    student = StudentSchoolRecord.query.get_or_404(student_id)
    grades = student.student_grades  # relationship from StudentSchoolRecord -> StudentGrade
    return render_template("grades/view_student_grades.html", student=student, grades=grades)


# ----------------- Create grade for a specific student -------------------
@dash_bp.route("/create_grade/<int:student_id>", methods=["GET", "POST"])
@role_required("teacher")
def create_grade(student_id):
    from dash.models import StudentGrade
    from auth.models import StudentSchoolRecord
    from flask import request

    student = StudentSchoolRecord.query.get_or_404(student_id)

    if request.method == "POST":
        exam_name = request.form.get("exam_name")
        exam_code = request.form.get("exam_code")
        exam_subject_name = request.form.get("exam_subject_name")
        student_score = request.form.get("student_score", type=int)
        student_grade = request.form.get("student_grade")

        # save to DB
        new_grade = StudentGrade(
            exam_name=exam_name,
            exam_code=exam_code,
            exam_subject_name=exam_subject_name,
            student_score=student_score,
            student_grade=student_grade,
            student_school_record_id=student.id
        )
        db.session.add(new_grade)
        db.session.commit()

        # pass success message to template
        return render_template("grades/create_grade.html", student=student, success="Grade added successfully.")

    return render_template("grades/create_grade.html", student=student)


# ----------------- View one grade -------------------
@dash_bp.route("/view_one_grade/<int:id>", methods=["GET"])
@role_required("teacher")
def view_one_grade(id):
    from dash.models import StudentGrade
    grade = StudentGrade.query.get_or_404(id)
    return render_template("grades/view_one_grade.html", grade=grade)


# ----------------- Update grade -------------------
@dash_bp.route("/update_grade/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def update_grade(id):
    from dash.models import StudentGrade
    from flask import request

    grade = StudentGrade.query.get_or_404(id)

    if request.method == "POST":
        grade.exam_name = request.form.get("exam_name")
        grade.exam_code = request.form.get("exam_code")
        grade.exam_subject_name = request.form.get("exam_subject_name")
        grade.student_score = request.form.get("student_score", type=int)
        grade.student_grade = request.form.get("student_grade")
        db.session.commit()
        return render_template("grades/update_grade.html", grade=grade, success="Grade updated successfully.")

    return render_template("grades/update_grade.html", grade=grade)


# ----------------- Delete grade -------------------
@dash_bp.route("/delete_grade/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def delete_grade(id):
    from dash.models import StudentGrade
    grade = StudentGrade.query.get_or_404(id)
    student_id = grade.student_school_record_id
    db.session.delete(grade)
    db.session.commit()
    return render_template("grades/delete_grade.html", success="Grade deleted successfully.", student_id=student_id)

# ------------------ Student Only------------------------
@dash_bp.route("/view_student_assignments", methods=["GET"])
@role_required("admin", "student")
def view_student_assignments():
    return render_template("student_only/view_student_assignments.html")


@dash_bp.route("/view_student_assignment_details/<int:id>", methods=["GET"])
@role_required("admin", "student")
def view_student_assignment_detail(id):
    return render_template("student_only/view_student_assignment_detail.html")


@dash_bp.route("/student_grades", methods=["GET"])
@role_required("admin", "student")
def student_grades():
    return render_template("student_only/student_grades.html")


@dash_bp.route("/student_grade_details/<int:id>", methods=["GET"])
@role_required("admin", "student")
def student_grade_details(id):
    return render_template("student_only/student_grade_detail.html")

# -------------------------- Student Attentance --------------------------------
from flask import request

@dash_bp.route("/attendance/students", methods=["GET"])
@role_required("teacher", "admin")
def view_attendance_students():
    from auth.models import StudentSchoolRecord

    # Get current page and per_page from query params
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)  # default 10 entries per page

    students_paginated = StudentSchoolRecord.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        "attendance/view_attendance_students.html", 
        students=students_paginated
    )



@dash_bp.route("/attendance/student/<int:id>", methods=["GET"])
@role_required("teacher", "admin")
def view_student_attendance(id):
    from auth.models import StudentSchoolRecord

    student = StudentSchoolRecord.query.get_or_404(id)
    attendances = student.student_attendances
    return render_template("attendance/view_student_attendance.html",
                           student=student, attendances=attendances)

@dash_bp.route("/attendance/create/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def create_attendance(id):
    from dash.models import StudentAttendance
    from auth.models import StudentSchoolRecord
    from flask import request
    from datetime import date

    student = StudentSchoolRecord.query.get_or_404(id)

    if request.method == "POST":
        status = request.form.get("status")  # Present / Absent
        today = date.today()

        # Prevent duplicate attendance for the same date
        existing = StudentAttendance.query.filter_by(
            student_school_record_id=student.id,
            attendance_date=today
        ).first()

        if existing:
            return render_template("attendance/create_attendance.html",
                                   student=student,
                                   error="Attendance for today already exists!")

        new_att = StudentAttendance(
            status=status,
            attendance_date=today,
            student_school_record_id=student.id
        )
        db.session.add(new_att)
        db.session.commit()

        return render_template("attendance/create_attendance.html",
                               student=student,
                               success="Attendance recorded successfully!")

    return render_template("attendance/create_attendance.html", student=student)


@dash_bp.route("/attendance/update/<int:id>", methods=["GET", "POST"])
@role_required("teacher", "admin")
def update_attendance(id):
    from dash.models import StudentAttendance
    from flask import request

    attendance = StudentAttendance.query.get_or_404(id)

    if request.method == "POST":
        attendance.status = request.form.get("status")
        db.session.commit()
        return render_template("attendance/update_attendance.html",
                               attendance=attendance,
                               success="Attendance updated successfully!")

    return render_template("attendance/update_attendance.html", attendance=attendance)

@dash_bp.route("/attendance/delete/<int:id>", methods=["GET"])
@role_required("teacher", "admin")
def delete_attendance(id):
    from dash.models import StudentAttendance

    attendance = StudentAttendance.query.get_or_404(id)
    student_id = attendance.student_school_record_id

    db.session.delete(attendance)
    db.session.commit()

    return render_template("attendance/delete_attendance.html",
                           success="Attendance deleted successfully!",
                           student_id=student_id)


# ------------------------------- CHAT BOT --------------------------

@dash_bp.route('/chatbot', methods=['POST'])
def chatbot():
    req = request.get_json()
    msg = req.get('message')

    if any(word in msg for word in ["Hello","Hi"]):
        return choice(chat_bot_responses["greeting"])

    # compute response...
    return jsonify(reply="Hi there how can i help")


# ------------------ Profile ------------------------
@dash_bp.route("/view_profile", methods=["GET"])
@role_required("teacher", "admin", "student")
def view_profile():
    return render_template("profile/view_profile.html")


@dash_bp.route("/update_account_password/<int:id>", methods=["POST"])
@role_required("teacher", "admin", "student")
def update_account_password(id):
    return redirect(url_for('view_profile'))


@dash_bp.route("/settings", methods=["GET"])
@role_required("teacher", "admin")
def settings():
    return render_template("profile/settings.html")
