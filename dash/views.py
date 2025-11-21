from flask import Blueprint, render_template, redirect, url_for
from . import dash_bp



# --------------- Use Here Only ----------------------------------


@dash_bp.route("/")
def index():
    return render_template("index.html")


# ------------------ Student Management End-Points ------------------------
@dash_bp.route("/create_student", methods=["GET", "POST"])
def create_student():
    return render_template("student_management/create_student.html")


@dash_bp.route("/view_students", methods=["GET", "POST"])
def view_students():
    return render_template("student_management/view_students.html")


@dash_bp.route("/view_one_student/<int:id>", methods=["GET", "POST"])
def view_one_student(id):
    return render_template("student_management/view_one_student.html")


@dash_bp.route("/update_student/<int:id>", methods=["GET", "POST"])
def update_student(id):
    return render_template("student_management/update_student.html")


@dash_bp.route("/delete_student/<int:id>", methods=["GET", "POST"])
def delete_student(id):
    return render_template("student_management/delete_student.html")


# ------------------ Assignments End-Points ------------------------
@dash_bp.route("/create_assignment", methods=["GET", "POST"])
def create_assignment():
    return render_template("assignment/create_assignment.html")


@dash_bp.route("/view_assignments", methods=["GET", "POST"])
def view_assignment():
    return render_template("assignment/view_assignments.html")


@dash_bp.route("/view_one_assignment/<int:id>", methods=["GET", "POST"])
def view_one_assignment(id):
    return render_template("student_management/view_one_assignment.html")


@dash_bp.route("/update_assignment/<int:id>", methods=["GET", "POST"])
def update_assignment(id):
    return render_template("assignment/update_assignment.html")


@dash_bp.route("/delete_assignment/<int:id>", methods=["GET", "POST"])
def delete_assignment(id):
    return render_template("assignment/delete_assignment.html")


# ------------------ Attendance End-Points ------------------------
@dash_bp.route("/create_attendance", methods=["GET", "POST"])
def create_attendance():
    return render_template("attendance/create_attendance.html")


@dash_bp.route("/view_attendances", methods=["GET", "POST"])
def view_attendances():
    return render_template("attendance/view_attendances.html")


@dash_bp.route("/view_one_attendance/<int:id>", methods=["GET", "POST"])
def view_one_attendance(id):
    return render_template("attendance/view_one_attendance.html")


@dash_bp.route("/update_attendance/<int:id>", methods=["GET", "POST"])
def update_attendance(id):
    return render_template("attendance/update_attendance.html")


@dash_bp.route("/delete_attendance/<int:id>", methods=["GET", "POST"])
def delete_attendance(id):
    return render_template("attendance/delete_attendance.html")


# ------------------ Grade End-Points ------------------------
@dash_bp.route("/create_grade", methods=["GET", "POST"])
def create_grade():
    return render_template("grades/create_grade.html")


@dash_bp.route("/view_grades", methods=["GET", "POST"])
def view_grades():
    return render_template("grades/view_grades.html")


@dash_bp.route("/view_one_grade/<int:id>", methods=["GET", "POST"])
def view_one_grade(id):
    return render_template("grades/view_one_grade.html")


@dash_bp.route("/update_grade/<int:id>", methods=["GET", "POST"])
def update_grade(id):
    return render_template("grades/update_grade.html")


@dash_bp.route("/delete_grade/<int:id>", methods=["GET", "POST"])
def delete_grade(id):
    return render_template("grades/delete_grade.html")


# ------------------ Student Only------------------------
@dash_bp.route("/view_student_assignments", methods=["GET"])
def view_student_assignments():
    return render_template("student_only/view_student_assignments.html")


@dash_bp.route("/view_student_assignment_details/<int:id>", methods=["GET"])
def view_student_assignment_detail(id):
    return render_template("student_only/view_student_assignment_detail.html")


@dash_bp.route("/view_student_grades", methods=["GET"])
def view_student_grades():
    return render_template("student_only/view_student_grades.html")


@dash_bp.route("/view_student_grade_details/<int:id>", methods=["GET"])
def view_student_grade_details(id):
    return render_template("student_only/view_student_grade_detail.html")


@dash_bp.route("/view_student_attendances", methods=["GET"])
def view_student_attendances():
    return render_template("student_only/view_student_attendances.html")


@dash_bp.route("/view_student_attendance_details/<int:id>", methods=["GET"])
def view_student_attendances_details(id):
    return render_template("student_only/view_student_attendance_detail.html")
