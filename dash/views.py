from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import desc,asc,text
from extensions import db

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
    if not current_user.is_authenticated:
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
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            # User logged in but wrong role → Forbidden
            if current_user.role not in roles:
                return abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator





@dash_bp.route("/")
@role_required("teacher","admin")
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
@dash_bp.route("/create_student", methods=["GET", "POST"])
@role_required("teacher","admin")
def create_student():
    
    return render_template("student_management/create_student.html")


@dash_bp.route("/view_students", methods=["GET", "POST"])
@role_required("teacher","admin")
def view_students():
    from auth.models import StudentSchoolRecord
    students = StudentSchoolRecord.query.all()
    return render_template("student_management/view_students.html", students=students)


@dash_bp.route("/view_one_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def view_one_student(id):
    return render_template("student_management/view_one_student.html")


@dash_bp.route("/update_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def update_student(id):
    return render_template("student_management/update_student.html")


@dash_bp.route("/delete_student/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def delete_student(id):
    return render_template("student_management/delete_student.html")


# ------------------ Assignments End-Points ------------------------ [Teacher & Admin]
@dash_bp.route("/create_assignment", methods=["GET", "POST"])
@role_required("teacher")
def create_assignment():

    return render_template("assignment/create_assignment.html")


@dash_bp.route("/view_assignments", methods=["GET", "POST"])
@role_required("teacher","admin")
def view_assignment():
    return render_template("assignment/view_assignments.html")


@dash_bp.route("/view_one_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin","student")
def view_one_assignment(id):
    return render_template("student_management/view_one_assignment.html")


@dash_bp.route("/update_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def update_assignment(id):
    return render_template("assignment/update_assignment.html")



@dash_bp.route("/delete_assignment/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def delete_assignment(id):
    return render_template("assignment/delete_assignment.html")

# ------------------------------- Assignment Submission [Teacher] ----------------------
@dash_bp.route("/view_assignment_submissions", methods=["GET", "POST"])
@role_required("teacher")
def teacher_view_assignment_submissions():
    return render_template("student_assignment_submission/view_student_assigment_submission.html")


@dash_bp.route("/view_one_assignment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def  teacher_view_one_assignment_submission(id):
    return render_template("student_assignment_submission/view_one_student_assigment_submission_detail.html")


@dash_bp.route("/update_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def  teacher_update_assigment_submission(id):
    return render_template("student_assignment_submission/update_student_assigment_submission.html")


@dash_bp.route("/delete_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def  teacher_delete_assigment_submission(id):
    return render_template("student_assignment_submission/delete_student_assigment_submission.html")



# ------------------ Assignment Submission End-Points ------------------------
@dash_bp.route("/create_assignment_submission", methods=["GET", "POST"])
@role_required("admin","student")
def create_assignment_submission():
  
    return render_template("student_assignment_submission/create_student_assigment_submission.html")


@dash_bp.route("/view_assignment_submissions", methods=["GET", "POST"])
@role_required("admin","student")
def view_assignment_submissions():
    return render_template("student_assignment_submission/view_student_assigment_submission.html")


@dash_bp.route("/view_one_assignment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin","student")
def view_one_assignment_submission(id):
    return render_template("student_assignment_submission/view_one_student_assigment_submission_detail.html")


@dash_bp.route("/update_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin","student")
def update_assigment_submission(id):
    return render_template("student_assignment_submission/update_student_assigment_submission.html")


@dash_bp.route("/delete_assigment_submission/<int:id>", methods=["GET", "POST"])
@role_required("admin","student")
def delete_assigment_submission(id):
    return render_template("student_assignment_submission/delete_student_assigment_submission.html")



# ------------------ Attendance End-Points ------------------------
@dash_bp.route("/create_attendance", methods=["GET", "POST"])
@role_required("teacher","admin")
def create_attendance():
   
    return render_template("attendance/create_attendance.html")


@dash_bp.route("/view_attendances", methods=["GET", "POST"])
@role_required("teacher","admin")
def view_attendances():
    return render_template("attendance/view_attendances.html")


@dash_bp.route("/view_one_attendance/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def view_one_attendance(id):
    return render_template("attendance/view_one_attendance.html")


@dash_bp.route("/update_attendance/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def update_attendance(id):
    return render_template("attendance/update_attendance.html")


@dash_bp.route("/delete_attendance/<int:id>", methods=["GET", "POST"])
@role_required("teacher","admin")
def delete_attendance(id):
    return render_template("attendance/delete_attendance.html")


# ------------------ Grade End-Points ------------------------
@dash_bp.route("/create_grade", methods=["GET", "POST"])
@role_required("teacher")
def create_grade():
   
    return render_template("grades/create_grade.html")


@dash_bp.route("/view_grades", methods=["GET", "POST"])
@role_required("teacher")
def view_grades():
    return render_template("grades/view_grades.html")


@dash_bp.route("/view_one_grade/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def view_one_grade(id):
    return render_template("grades/view_one_grade.html")


@dash_bp.route("/update_grade/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def update_grade(id):
    return render_template("grades/update_grade.html")


@dash_bp.route("/delete_grade/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def delete_grade(id):
    return render_template("grades/delete_grade.html")


# ------------------ Student Only------------------------
@dash_bp.route("/view_student_assignments", methods=["GET"])
@role_required("admin","student")
def view_student_assignments():
    return render_template("student_only/view_student_assignments.html")


@dash_bp.route("/view_student_assignment_details/<int:id>", methods=["GET"])
@role_required("admin","student")
def view_student_assignment_detail(id):
    return render_template("student_only/view_student_assignment_detail.html")


@dash_bp.route("/view_student_grades", methods=["GET"])
@role_required("admin","student")
def view_student_grades():
    return render_template("student_only/view_student_grades.html")


@dash_bp.route("/view_student_grade_details/<int:id>", methods=["GET"])
@role_required("admin","student")
def view_student_grade_details(id):
    return render_template("student_only/view_student_grade_detail.html")


@dash_bp.route("/view_student_attendances", methods=["GET"])
@role_required("admin","student")
def view_student_attendances():
    return render_template("student_only/view_student_attendances.html")


@dash_bp.route("/view_student_attendance_details/<int:id>", methods=["GET"])
@role_required("admin","student")
def view_student_attendances_details(id):
    return render_template("student_only/view_student_attendance_detail.html")


# ------------------ Profile ------------------------
@dash_bp.route("/view_profile", methods=["GET"])
@role_required("teacher","admin","student")
def view_profile():
    return render_template("profile/view_profile.html")

@dash_bp.route("/update_account_password/<int:id>", methods=["POST"])
@role_required("teacher","admin","student")
def update_account_password(id):
    return redirect(url_for('view_profile'))

@dash_bp.route("/settings", methods=["GET"])
@role_required("teacher","admin")
def settings():
    return render_template("profile/settings.html")


