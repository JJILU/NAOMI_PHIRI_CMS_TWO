from flask import Blueprint,render_template,redirect,url_for


dash_bp = Blueprint("dash",__name__,template_folder="templates",static_folder="static")

# --------------- Use Here Only ----------------------------------
@dash_bp.route("/")
def index():
    return render_template("index.html")


# ------------------ Student Management End-Points ------------------------ 
@dash_bp.route("/create_student", methods=["GET","POST"])
def create_student():
    return render_template("student_management/create_student.html")


@dash_bp.route("/view_students", methods=["GET","POST"])
def view_students():
    return render_template("student_management/view_students.html")

@dash_bp.route("/view_one_student/<int:id>", methods=["GET","POST"])
def view_one_student(id):
    return render_template("student_management/view_one_student.html")


@dash_bp.route("/update_student/<int:id>", methods=["GET","POST"])
def update_student(id):
    return render_template("student_management/update_student.html")


@dash_bp.route("/delete_assignment", methods=["GET","POST"])
def delete_student():
    return render_template("student_management/delete_student.html")


# ------------------ Assignments End-Points ------------------------ 
@dash_bp.route("/create_assignment", methods=["GET","POST"])
def create_assignment():
    return render_template("assignment/create_assignment.html")


@dash_bp.route("/view_assignments", methods=["GET","POST"])
def view_assignment():
    return render_template("assignment/view_assignments.html")


@dash_bp.route("/view_one_assignment/<int:id>", methods=["GET","POST"])
def view_one_assignment(id):
    return render_template("student_management/view_one_assignment.html")


@dash_bp.route("/update_assignment", methods=["GET","POST"])
def update_assignment():
    return render_template("assignment/update_assignment.html")


@dash_bp.route("/delete_assignment", methods=["GET","POST"])
def delete_assignment():
    return render_template("assignment/delete_assignment.html")



# ------------------ Attendance End-Points ------------------------ 
@dash_bp.route("/create_attendance", methods=["GET","POST"])
def create_attendance():
    return render_template("attendance/create_attendance.html")


@dash_bp.route("/view_attendances", methods=["GET","POST"])
def view_attendances():
    return render_template("attendance/view_attendance.html")


@dash_bp.route("/update_attendance", methods=["GET","POST"])
def update_attendance():
    return render_template("attendance/update_attendance.html")



@dash_bp.route("/delete_attendance", methods=["GET","POST"])
def delete_attendance():
    return render_template("attendance/delete_attendance.html")


# ------------------ Grade End-Points ------------------------ 
@dash_bp.route("/create_grade", methods=["GET","POST"])
def create_grade():
    return render_template("grades/create_grade.html")


@dash_bp.route("/view_grade", methods=["GET","POST"])
def view_grade():
    return render_template("grades/view_grade.html")


@dash_bp.route("/update_grade", methods=["GET","POST"])
def update_grade():
    return render_template("grades/update_grade.html")



@dash_bp.route("/delete_grade", methods=["GET","POST"])
def delete_grade():
    return render_template("grades/delete_grade.html")