from flask import render_template, redirect, url_for, request, abort, jsonify, current_app,send_from_directory,session,request
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import desc, asc
from extensions import db,faker,socketio
from random import choice
import os
from werkzeug.utils import secure_filename
from datetime import datetime


from flask_socketio import SocketIO, join_room, leave_room, send




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


# Allowed extensions
ALLOWED_EXT = {"pdf", "doc", "docx", "png", "jpg", "jpeg", "gif","jfif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ----------------------- START LANDING PAGE --------------------------------------------
@dash_bp.route("/")
@login_required
def index():
    from dash.models import Classroom, ClassAssignment, StudentAttendance
    from auth.models import Student

    # Total counts
    total_students = Student.query.count()
    total_classes = Classroom.query.count()
    total_assignments = ClassAssignment.query.count()

    # Attendance %
    total_present = StudentAttendance.query.filter_by(status="Present").count()
    total_absent = StudentAttendance.query.filter_by(status="Absent").count()
    print(">> a>>",total_present,total_absent)
    total_attendance = total_present + total_absent

    present_percent = round((total_present / total_attendance) * 100, 1) if total_attendance else 0
    absent_percent = round((total_absent / total_attendance) * 100, 1) if total_attendance else 0

    # Chart.js data
    chart_labels = ["Total Students", "Attendance Today", "Assignments Submitted", "Pending Assignments"]
    chart_values = [total_students, total_present, total_assignments, total_assignments - total_present]

    # Flot.js example (daily data for 7 days)
    chart_total = [[i, total_students] for i in range(7)]
    chart_attendance = [[i, total_present // 7] for i in range(7)]
    chart_assignments = [[i, total_assignments // 7] for i in range(7)]
    chart_pending = [[i, (total_assignments - total_present) // 7] for i in range(7)]

    return render_template(
        "index.html",
        total_students=total_students,
        total_classes=total_classes,
        total_assignments=total_assignments,
        present_percent=present_percent,
        absent_percent=absent_percent,
        chart_labels=chart_labels,
        chart_values=chart_values,
        chart_total=chart_total,
        chart_attendance=chart_attendance,
        chart_assignments=chart_assignments,
        chart_pending=chart_pending
    ) 

# ----------------------- END LANDING PAGE --------------------------------------------



# ------------------ START ADMIN ENDPOINTS ------------------------
# -------------------------
# Serve profile photo
# -------------------------
@dash_bp.route("/uploads/profile_photo/<filename>")
def uploaded_avator_photo(filename):
    return send_from_directory(current_app.config["PROFILE_PHOTO_UPLOAD"], filename)


# -------------------------
# Create admin
# -------------------------
@dash_bp.route("/create_admin", methods=["GET", "POST"])
@role_required("teacher")
def create_admin():
    from auth.models import Student, StudentSchoolRecord
    from werkzeug.security import generate_password_hash
    error = None
    success = None

    # Fetch students who are marked as admin in school records
    admin_students = StudentSchoolRecord.query.filter_by(is_admin=True).all()

    if request.method == "POST":
        student_id = request.form.get("student_id")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or not confirm_password:
            error = "Both password fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            student = Student.query.filter_by(student_school_record_id=student_id).first()
            if not student:
                # Create new Student account
                student = Student(
                    user_card_id=StudentSchoolRecord.query.get(student_id).card_id,
                    password=password,
                    role="admin",
                    student_school_record_id=student_id
                )
                db.session.add(student)
            else:
                # Update password only
                student.hashed_password = generate_password_hash(password)

            db.session.commit()
            success = "Admin account created/updated successfully."
            return redirect(url_for("dash.view_admins"))

    return render_template("admin_management/create_admin.html",
                           card_ids=admin_students,
                           error=error,
                           success=success)


# -------------------------
# View all admins
# -------------------------
@dash_bp.route("/view_admins")
@role_required("teacher")
def view_admins():
    from auth.models import Student, StudentSchoolRecord
    admins = StudentSchoolRecord.query.filter(StudentSchoolRecord.is_admin==True).all()
    return render_template("admin_management/view_admins.html", admins=admins)


# -------------------------
# Update admin password
# -------------------------
@dash_bp.route("/update_admin/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def update_admin(id):
    from auth.models import Student, StudentSchoolRecord
    from werkzeug.security import generate_password_hash
    error = None
    success = None
    admin = Student.query.get_or_404(id)

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not password or not confirm_password:
            error = "Both password fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            admin.hashed_password = generate_password_hash(password)
            db.session.commit()
            success = "Admin password updated successfully."
            return redirect(url_for("dash.view_admins"))

    return render_template("admin_management/update_admin.html", admin=admin, error=error, success=success)


# -------------------------
# Delete admin
# -------------------------
@dash_bp.route("/delete_admin/<int:id>", methods=["GET", "POST"])
@role_required("teacher")
def delete_admin(id):
    from auth.models import Student
    error = None
    success = None
    admin = Student.query.get_or_404(id)

    if request.method == "POST":
        try:
            db.session.delete(admin)
            db.session.commit()
            success = "Admin deleted successfully."
            return redirect(url_for("dash.view_admins"))
        except Exception as e:
            error = str(e)

    return render_template("admin_management/delete_admin.html", admin=admin, error=error, success=success)
# ------------------ END ADMIN ENDPOINTS ------------------------



# ------------------ START STUDENT MANAGEMENT END-POINTS ------------------------
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
# ------------------ END STUDENT MANAGEMENT END-POINTS ------------------------



# ------------------ START CMS STUDENT END-POINTS ------------------------ 
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


# ------------------ END CMS STUDENT END-POINTS ------------------------ 



# ------------------ START ASSIGNMENT END-POINTS ------------------------ [Teacher & Admin]


# ------------------ LIST ASSIGNMENTS WITH PAGINATION ----------------------

@dash_bp.route("/assignments", methods=["GET"])
def list_assignments():
    from dash.models import ClassAssignment
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)  # default 6 per page

    pagination = ClassAssignment.query.order_by(
        ClassAssignment.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template("assignment/list_assignments.html",
                           pagination=pagination,
                           assignments=pagination.items,
                           per_page=per_page,
                           error=None,
                           success=None)

# ----------------------------------------------------
# 3. CREATE ASSIGNMENT
# ----------------------------------------------------
@dash_bp.route("/assignments/create", methods=["GET", "POST"])
def create_assignment():
    from dash.models import (
        ClassAssignment, AssignmentFileUpload,
        CompulsarySubject, OptionalSubject
    )
    from auth.models import TeacherSchoolRecord
    from extensions import db
    from flask import current_app, request, render_template
    import os
    from werkzeug.utils import secure_filename
    from datetime import datetime
    from flask_login import current_user

    # ------------------------------
    # Get teacher's subjects
    # ------------------------------
    teacher_record = TeacherSchoolRecord.query.filter_by(
        card_id=current_user.teacherschoolrecord.card_id # type: ignore
    ).first()

    compulsary_subs = teacher_record.compulsarysubject
    optional_subs = teacher_record.optionalsubject

    # Serialize subjects for JS
    compulsary_subs_json = [
        {"id": s.id, "subject_name": s.subject_name, "subject_code": s.subject_code}
        for s in compulsary_subs
    ]
    optional_subs_json = [
        {"id": s.id, "subject_name": s.subject_name, "subject_code": s.subject_code}
        for s in optional_subs
    ]

    print()

    error = None
    success = None

    if request.method == "POST":
        try:
            assignment_name = request.form.get("assignment_name").strip()
            subject_type = request.form.get("subject_type")
            subject_id = int(request.form.get("subject_id"))
            classroom_id = int(request.form.get("classroom_id"))
            due_date = request.form.get("due_date")

            created_date = datetime.utcnow().strftime("%Y-%m-%d")
            if due_date < created_date:
                error = "Due date must be greater than today's date."
                raise ValueError(error)

            # Get subject
            subject_cls = CompulsarySubject if subject_type == "compulsary" else OptionalSubject
            subject = subject_cls.query.get_or_404(subject_id)

            # Create assignment
            new_assign = ClassAssignment(
                assignment_name=assignment_name,
                assignment_subject_Name=subject.subject_name,
                assignment_subject_code=subject.subject_code,
                classroom_id=classroom_id
            )
            db.session.add(new_assign)
            db.session.commit()
            print(f"[DEBUG] Assignment created: {new_assign.assignment_name}")

            # Upload files
            files = request.files.getlist("files")
            upload_folder = current_app.config.get("ASSIGNMENT_UPLOAD", "uploads/assignments")
            os.makedirs(upload_folder, exist_ok=True)

            for f in files:
                if f.filename:
                    filename = secure_filename(f.filename)
                    dest = os.path.join(upload_folder, f"{datetime.utcnow().timestamp():.0f}_{filename}")
                    f.save(dest)

                    file_record = AssignmentFileUpload(
                        original_name=f.filename,
                        filename=os.path.basename(dest),
                        filepath=os.path.relpath(dest, start=os.getcwd()),
                        class_assignment_id=new_assign.id
                    )
                    db.session.add(file_record)

            db.session.commit()
            success = "Assignment created successfully."
            print("[DEBUG] Files uploaded and DB updated")

        except Exception as e:
            print("[DEBUG] Error creating assignment:", e)
            if not error:
                error = str(e)

    return render_template(
        "assignment/create_assignment.html",
        compulsary_subs=compulsary_subs_json,
        optional_subs=optional_subs_json,
        error=error,
        success=success
    )


# ----------------------------------------------------
# AJAX – GET CLASSROOMS FOR SUBJECT
# ----------------------------------------------------
@dash_bp.route("/subject/<subject_type>/<int:subject_id>/classrooms", methods=["GET"])
def get_subject_classrooms(subject_type, subject_id):
    from dash.models import CompulsarySubject, OptionalSubject
    from flask import jsonify

    print(f"[DEBUG] Classroom request: subject_type={subject_type}, subject_id={subject_id}")

    subject_cls = CompulsarySubject if subject_type == "compulsary" else OptionalSubject
    subject = subject_cls.query.get(subject_id)
    if not subject:
        print(f"[DEBUG] Subject NOT found for id={subject_id}")
        return jsonify([])

    if hasattr(subject, "classrooms"):
        classrooms = subject.classrooms.all() if hasattr(subject.classrooms, "all") else subject.classrooms
        classrooms_data = [{"id": c.id, "classroom_name": c.classroom_name} for c in classrooms]
        print(f"[DEBUG] Classrooms loaded: {classrooms_data}")
    else:
        classrooms_data = []
        print("[DEBUG] Subject has no classrooms attribute")

        print("my debug classes", classrooms_data)

    return jsonify(classrooms_data)





# ----------------------------------------------------
# 4. UPDATE ASSIGNMENT
# ----------------------------------------------------
@dash_bp.route("/assignments/<int:id>/update", methods=["GET", "POST"])
def update_assignment(id):
    from dash.models import ClassAssignment, AssignmentFileUpload
    from extensions import db

    assignment = ClassAssignment.query.get_or_404(id)
    error = None
    success = None

    if request.method == "POST":
        assignment.assignment_name = request.form.get("assignment_name").strip()
        db.session.commit()

        files = request.files.getlist("files")
        upload_folder = current_app.config.get("ASSIGNMENT_UPLOAD", "uploads/assignments")
        os.makedirs(upload_folder, exist_ok=True)

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                dest = os.path.join(upload_folder, f"{datetime.utcnow().timestamp():.0f}_{filename}")
                f.save(dest)

                file_record = AssignmentFileUpload(
                    original_name=f.filename,
                    filename=os.path.basename(dest),
                    filepath=os.path.relpath(dest, start=os.getcwd()),
                    class_assignment_id=assignment.id
                )
                db.session.add(file_record)

        db.session.commit()
        success = "Assignment updated successfully."

    return render_template("assignment/update_assignment.html",
                           assignment=assignment,
                           error=error,
                           success=success)

# ----------------------------------------------------
# 5. DELETE ASSIGNMENT
# ----------------------------------------------------
# DELETE CONFIRMATION PAGE
@dash_bp.route("/assignments/<int:id>/delete", methods=["GET", "POST"])
def delete_assignment(id):
    from dash.models import ClassAssignment, AssignmentFileUpload
    from extensions import db

    assignment = ClassAssignment.query.get_or_404(id)

    if request.method == "POST":
        # Delete files
        for f in assignment.assignment_file_uploads:
            try:
                path = os.path.join(os.getcwd(), f.filepath)
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
            db.session.delete(f)

        db.session.delete(assignment)
        db.session.commit()
        return redirect(url_for("dash.list_assignments"))

    # GET request shows confirmation page
    return render_template("assignment/delete_assignment.html", assignment=assignment)


# ----------------------------------------------------
# 6. VIEW ONE ASSIGNMENT
# ----------------------------------------------------
@dash_bp.route("/assignments/<int:id>", methods=["GET"])
def view_assignment(id):
    from dash.models import ClassAssignment
    assignment = ClassAssignment.query.get_or_404(id)
    return render_template("assignment/view_assignment.html",
                           assignment=assignment,
                           error=None,
                           success=None)

# ----------------------------------------------------
# 7. DOWNLOAD FILE
# ----------------------------------------------------
@dash_bp.route("/assignments/file/<int:file_id>/download", methods=["GET"])
def download_file(file_id):
    from dash.models import AssignmentFileUpload

    file_rec = AssignmentFileUpload.query.get_or_404(file_id)
    path = os.path.join(os.getcwd(), file_rec.filepath)

    return send_from_directory(
        os.path.dirname(path),
        os.path.basename(path),
        as_attachment=True
    )


# ------------------ END ASSIGNMENT END-POINTS ------------------------ [Teacher & Admin]


# ------------------ START ASSIGNMENT SUBMISSIION END-POINTS ------------------------ [Teacher & Admin]

# ------------------------------- Assignment Submission [Teacher] ----------------------

# ---------- Student: create/view/update/delete submissions ----------
@dash_bp.route("/student/assignments", methods=["GET", "POST"])
@role_required("student","admin")
def student_submission_assignments():
    # imports inside route
    from dash.models import ClassAssignment, StudentAssignmentSubmission, AssignmentSubmisssionFileUpload
    from werkzeug.utils import secure_filename
    from flask import current_app

    error = None
    success = None

    # ----------------------------------------------------
    # FIXED: Determine student_school_record safely
    # ----------------------------------------------------
    if hasattr(current_user, "student") and current_user.student:
        # logged in user is a Student
        student_record = current_user.student

    elif hasattr(current_user, "admin") and current_user.admin:
        # logged in user is an Admin
        student_record = current_user.admin

    else:
        return redirect(url_for("dash.index"))

    # ----------------------------------------------------
    # Get classroom from student_record
    # ----------------------------------------------------
    classroom = getattr(student_record, "classroom", None)

    if not classroom:
        assignments = []
    else:
        assignments = (
            ClassAssignment.query
            .filter_by(classroom_id=classroom.id)
            .order_by(ClassAssignment.created_at.desc())
            .all()
        )

    # ----------------------------------------------------
    # Handle submission POST
    # ----------------------------------------------------
    if request.method == "POST":
        assignment_id = request.form.get("assignment_id")
        files = request.files.getlist("assignment_files")

        if not assignment_id:
            error = "Please select an assignment."
        elif not files or files[0].filename == "":
            error = "Please upload at least one file."
        else:
            try:
                assignment_id = int(assignment_id)
            except:
                error = "Invalid assignment selected."
                assignment_id = None

            if assignment_id:
                class_assignment = ClassAssignment.query.get(assignment_id)

                if not class_assignment or class_assignment.classroom_id != classroom.id:
                    error = "You cannot submit to that assignment."
                else:
                    try:
                        submission = StudentAssignmentSubmission(
                            assignment_name=class_assignment.assignment_name,
                            assignment_subject_Name=class_assignment.assignment_subject_Name,
                            assignment_subject_code=class_assignment.assignment_subject_code,
                            student_school_record_id=student_record.id,
                            class_assignment_id=assignment_id,
                            submitted_by_first_name=student_record.first_name,
                            submitted_by_last_name=student_record.last_name,
                        )

                        db.session.add(submission)
                        db.session.flush()  # get ID before commit

                        upload_folder = current_app.config.get("STUDENT_SUBMISSION_UPLOAD")
                        os.makedirs(upload_folder, exist_ok=True) # type: ignore

                        for f in files:
                            if f and allowed_file(f.filename):
                                filename = secure_filename(f.filename) # type: ignore
                                dest = os.path.join(upload_folder, f"{int(datetime.utcnow().timestamp())}_{filename}") # type: ignore
                                f.save(dest)

                                file_record = AssignmentSubmisssionFileUpload(
                                    original_name=f.filename,
                                    filename=os.path.basename(dest),
                                    filepath=dest,
                                    student_assignment_submission_id=submission.id
                                )
                                db.session.add(file_record)

                        db.session.commit()
                        success = "Assignment submitted successfully!"

                    except Exception as e:
                        db.session.rollback()
                        error = "Failed to submit assignment. " + str(e)

    # ----------------------------------------------------
    # Paginated submissions for current student/admin
    # ----------------------------------------------------
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    submissions_q = (
        StudentAssignmentSubmission.query
        .filter_by(student_school_record_id=student_record.id)
        .order_by(StudentAssignmentSubmission.created_at.desc())
    )

    submissions_paginated = submissions_q.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "student_assignment_submission/create_student_assigment_submission.html",
        assignments=assignments,
        submissions=submissions_paginated.items,
        pagination=submissions_paginated,
        per_page=per_page,
        error=error,
        success=success
    )



@dash_bp.route("/student/assignments/<int:submission_id>/view", methods=["GET"])
@login_required
@role_required("student","admin")
def student_view_submission(submission_id):
    from dash.models import StudentAssignmentSubmission
    # ensure student owns this submission
    submission = StudentAssignmentSubmission.query.get_or_404(submission_id)
    if submission.student_school_record_id != current_user.student.id:
        abort(403)
    return render_template("student_assignment_submission/view_one_student_assigment_submission_detail.html", submission=submission)


@dash_bp.route("/student/assignments/<int:submission_id>/update", methods=["GET", "POST"])
@login_required
@role_required("student")
def student_update_submission(submission_id):
    from dash.models import StudentAssignmentSubmission, AssignmentSubmisssionFileUpload
    from werkzeug.utils import secure_filename
    from flask import current_app

    submission = StudentAssignmentSubmission.query.get_or_404(submission_id)
    if submission.student_school_record_id != current_user.student.id:
        abort(403)

    error = None
    success = None

    if request.method == "POST":
        # allow uploading additional files (we won't remove existing files here)
        files = request.files.getlist("assignment_files")
        upload_folder = current_app.config.get("STUDENT_SUBMISSION_UPLOAD")
        os.makedirs(upload_folder, exist_ok=True) # type: ignore

        try:
            for f in files:
                if f and f.filename and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    dest = os.path.join(upload_folder, f"{int(datetime.utcnow().timestamp())}_{filename}") # type: ignore
                    f.save(dest)
                    file_record = AssignmentSubmisssionFileUpload(
                        original_name=f.filename,
                        filename=os.path.basename(dest),
                        filepath=dest,
                        student_assignment_submission_id=submission.id
                    )
                    db.session.add(file_record)
            db.session.commit()
            success = "Submission updated (files added)."
        except Exception as e:
            db.session.rollback()
            error = "Failed to update submission. " + str(e)

    return render_template("student_assignment_submission/update_student_assigment_submission.html", submission=submission, error=error, success=success)


@dash_bp.route("/student/assignments/<int:submission_id>/delete", methods=["POST"])
@login_required
@role_required("student")
def student_delete_submission(submission_id):
    from dash.models import StudentAssignmentSubmission
    submission = StudentAssignmentSubmission.query.get_or_404(submission_id)
    if submission.student_school_record_id != current_user.student.id:
        abort(403)

    error = None
    success = None
    try:
        # delete files on disk
        for f in submission.assignment_submisssion_file_uploads:
            try:
                if os.path.exists(f.filepath):
                    os.remove(f.filepath)
            except Exception:
                pass
            db.session.delete(f)

        db.session.delete(submission)
        db.session.commit()
        success = "Submission deleted successfully."
    except Exception as e:
        db.session.rollback()
        error = "Failed to delete submission. " + str(e)

    # reload student's assignments page
    return redirect(url_for("dash.student_submission_assignments"))


# ---------- Teacher: view class assignments & submissions + grade update ----------
@dash_bp.route("/teacher/class-assignments", methods=["GET"])
@login_required
@role_required("teacher")
def teacher_class_assignments():
    from dash.models import ClassAssignment
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # NOTE: If you have teacher -> classroom mapping, filter here by classroom ids the teacher teaches.
    # Example: classroom_ids = [c.id for c in current_user.teacherschoolrecord.classrooms]
    # assignments_q = ClassAssignment.query.filter(ClassAssignment.classroom_id.in_(classroom_ids))
    assignments_q = ClassAssignment.query.order_by(ClassAssignment.created_at.desc())
    pagination = assignments_q.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("teacher_manage_assignment_submission/teacher_class_assignments.html",
                           assignments=pagination.items, pagination=pagination, per_page=per_page)


@dash_bp.route("/teacher/assignments/<int:assignment_id>/submissions", methods=["GET"])
@login_required
@role_required("teacher")
def teacher_view_all_submissions(assignment_id):
    from dash.models import ClassAssignment, StudentAssignmentSubmission
    assignment = ClassAssignment.query.get_or_404(assignment_id)

    # optionally ensure teacher allowed to view this assignment (if teacher-classroom mapping exists)
    # if assignment.classroom_id not in teacher_classroom_ids:
    #     abort(403)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    subs_q = StudentAssignmentSubmission.query.filter_by(class_assignment_id=assignment.id).order_by(StudentAssignmentSubmission.created_at.desc())
    pagination = subs_q.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("teacher_manage_assignment_submission/teacher_view_submissions.html",
                           assignment=assignment,
                           submissions=pagination.items,
                           pagination=pagination,
                           per_page=per_page)


@dash_bp.route("/teacher/submissions/<int:submission_id>/grade", methods=["GET", "POST"])
@login_required
@role_required("teacher")
def teacher_grade_one_submission(submission_id):
    from dash.models import StudentAssignmentSubmission
    from werkzeug.security import generate_password_hash  # not used but keep imports grouped
    submission = StudentAssignmentSubmission.query.get_or_404(submission_id)

    error = None
    success = None

    if request.method == "POST":
        try:
            score = request.form.get("student_score", type=int)
            grade = request.form.get("student_grade", "").strip()
            if score is None:
                error = "Score is required."
            else:
                submission.student_score = score
                submission.student_grade = grade or submission.student_grade
                db.session.commit()
                success = "Score and grade updated."
                # redirect back to submissions list for the assignment
                return redirect(url_for("dash.teacher_view_all_submissions", assignment_id=submission.class_assignment_id))
        except Exception as e:
            db.session.rollback()
            error = "Failed to update grade. " + str(e)

    return render_template("teacher_manage_assignment_submission/teacher_update_score.html", submission=submission, error=error, success=success)


# ---------- Admin: view submissions for their classroom (admin is a student + admin) ----------
@dash_bp.route("/admin/class-submissions", methods=["GET"])
@login_required
@role_required("admin")
def admin_view_class_submissions():
    from dash.models import StudentAssignmentSubmission, ClassAssignment

    # Admin model instance → linked to StudentSchoolRecord
    student_record = current_user.student_school_record_id

    if not student_record:
        abort(403)

    classroom = getattr(student_record, "classroom", None)
    if not classroom:
        submissions = []
        pagination = None
        per_page = request.args.get("per_page", 10, type=int)
        return render_template(
            "admin_view_assignments_submission/admin_view_submissions.html",
            submissions=submissions,
            pagination=pagination,
            per_page=per_page,
            classroom=None
        )

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # ✅ FIXED JOIN
    subs_q = (
        StudentAssignmentSubmission.query
        .join(ClassAssignment)  # correct join
        .filter(ClassAssignment.classroom_id == classroom.id)
        .order_by(StudentAssignmentSubmission.created_at.desc())
    )

    pagination = subs_q.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "admin_view_assignments_submission/admin_view_submissions.html",
        submissions=pagination.items,
        pagination=pagination,
        per_page=per_page,
        classroom=classroom
    )
# ------------------ END ASSIGNMENT SUBMISSIION END-POINTS ------------------------ [Teacher & Admin]





# -------------------- START GRADE -----------------------------------------------------------------

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

# ==============================================================================================================

# ------------------ Student/Admin Only: -------------


# -------------------- Grades List --------------------
@dash_bp.route("/grades", methods=["GET"])
@role_required("student", "admin")
def view_all_grades():
    from dash.models import StudentGrade
    student_record = getattr(current_user, "student_school_record", None)
    if not student_record:
        return render_template("student_only/grades.html", grades=[], pagination=None, per_page=10, error="No student record found")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    grades_query = StudentGrade.query.filter_by(student_school_record_id=student_record.id)\
                                     .order_by(StudentGrade.created_at.desc())
    grades_paginated = grades_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("student_only/grades.html",
                           grades=grades_paginated.items,
                           pagination=grades_paginated,
                           per_page=per_page,
                           error=None,
                           success=None)


# -------------------- Grade Detail --------------------
@dash_bp.route("/grades/<int:id>", methods=["GET"])
@role_required("student", "admin")
def grade_detail(id):
    from dash.models import StudentGrade
    student_record = getattr(current_user, "student_school_record", None)
    grade = StudentGrade.query.get_or_404(id)
    if grade.student_school_record_id != student_record.id:
        abort(403)
    return render_template("student_only/grade_detail.html", grade=grade, error=None, success=None)

# -------------------- END GRADE -----------------------------------------------------------------


# -------------------- START ASSIGNMENT ----------------------------------------------------------

# -------------------- Attendances List --------------------
@dash_bp.route("/attendances", methods=["GET"])
@role_required("student", "admin")
def view_attendances():
    from dash.models import StudentAttendance
    student_record = getattr(current_user, "student_school_record", None)
    if not student_record:
        return render_template("student_only/attendances.html", attendances=[], pagination=None, per_page=10, error="No student record found")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    attendances_query = StudentAttendance.query.filter_by(student_school_record_id=student_record.id)\
                                               .order_by(StudentAttendance.attendance_date.desc())
    attendances_paginated = attendances_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("student_only/attendances.html",
                           attendances=attendances_paginated.items,
                           pagination=attendances_paginated,
                           per_page=per_page,
                           error=None,
                           success=None)


# -------------------- Attendance Detail --------------------
@dash_bp.route("/attendances/<int:id>", methods=["GET"])
@role_required("student", "admin","teacher")
def attendance_detail(id):
    from dash.models import StudentAttendance
    student_record = getattr(current_user, "student_school_record", None)
    attendance = StudentAttendance.query.get_or_404(id)
    if attendance.student_school_record_id != student_record.id:
        abort(403)
    return render_template("student_only/attendance_detail.html", attendance=attendance, error=None, success=None)


# -------------------- Class Assignments List --------------------
@dash_bp.route("/class_assignments", methods=["GET"])
@role_required("student", "admin")
def view_class_assignments():
    from dash.models import ClassAssignment
    student_record = getattr(current_user, "student_school_record", None)
    if not student_record or not getattr(student_record, "classroom", None):
        return render_template("student_only/class_assignments.html", assignments=[], pagination=None, per_page=10, error="No classroom assigned")

    classroom_id = student_record.classroom.id
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    assignments_query = ClassAssignment.query.filter_by(classroom_id=classroom_id)\
                                             .order_by(ClassAssignment.created_at.desc())
    assignments_paginated = assignments_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("student_only/class_assignments.html",
                           assignments=assignments_paginated.items,
                           pagination=assignments_paginated,
                           per_page=per_page,
                           error=None,
                           success=None)


# -------------------- Assignment Submissions List --------------------
@dash_bp.route("/assignment_submissions", methods=["GET"])
@role_required("student", "admin")
def view_assignment_submissions():
    from dash.models import StudentAssignmentSubmission
    student_record = getattr(current_user, "student_school_record", None)
    if not student_record:
        return render_template("student_only/assignment_submissions.html", submissions=[], pagination=None, per_page=10, error="No student record found")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    submissions_query = StudentAssignmentSubmission.query.filter_by(student_school_record_id=student_record.id)\
                                                        .order_by(StudentAssignmentSubmission.created_at.desc())
    submissions_paginated = submissions_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("student_only/assignment_submissions.html",
                           submissions=submissions_paginated.items,
                           pagination=submissions_paginated,
                           per_page=per_page,
                           error=None,
                           success=None)


# -------------------- Assignment Submission Detail --------------------
@dash_bp.route("/assignment_submissions/<int:id>", methods=["GET"])
@role_required("student", "admin")
def assignment_submission_detail(id):
    from dash.models import StudentAssignmentSubmission
    student_record = getattr(current_user, "student_school_record", None)
    submission = StudentAssignmentSubmission.query.get_or_404(id)
    if submission.student_school_record_id != student_record.id:
        abort(403)
    return render_template("student_only/assignment_submission_detail.html", submission=submission, error=None, success=None)

# -------------------- END ASSIGNMENT ----------------------------------------------------------


# -------------------- START ATTENDNACE ----------------------------------------------------------


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

@dash_bp.route("/attendance/one_attendnce/<int:id>", methods=["GET"])
@role_required("teacher", "admin")
def view_one_attendance(id):
    from dash.models import StudentAttendance
    from flask import request

    attendance = StudentAttendance.query.get_or_404(id)
    return render_template("attendance/view_one_attendance.html", attendance=attendance)

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

    try:
        db.session.delete(attendance)
        db.session.commit()

        return render_template("attendance/delete_attendance.html",
                            success="Attendance deleted successfully!",
                            student_id=student_id)
    except Exception as e:
        db.session.rollback()
        return render_template("attendance/delete_attendance.html",
                            success="Failed To Delete Attendance, Server Error Occurred",
                            student_id=student_id)


# -------------------- END ATTENDANCE ----------------------------------------------------------



# -------------------- START CHAT-BOT ----------------------------------------------------------

from dash.chat_responses import chat_bot_responses
import re


@dash_bp.route('/chatbot', methods=['POST'])
def chatbot():
    req = request.get_json()
    msg = req.get('message', '').lower()

    # ========================= MESSAGE MATCHING =========================
    reply = None

    # BASIC GREETINGS
    if re.search(r"\b(hello|hi|hey|good morning|good afternoon)\b", msg):
        reply = choice(chat_bot_responses["greeting"])

    # AUTHENTICATION
    elif "login" in msg or "sign in" in msg:
        reply = choice(chat_bot_responses["auth"])
    elif "logout" in msg or "sign out" in msg:
        reply = choice(chat_bot_responses["logout"])

    # DASHBOARD
    elif "dashboard" in msg:
        reply = choice(chat_bot_responses["dashboard"])

    # PROFILE
    elif "profile" in msg or "update profile" in msg:
        reply = choice(chat_bot_responses["profile"])

    # STUDENT / TEACHER / ADMIN MANAGEMENT
    elif "student" in msg:
        reply = choice(chat_bot_responses["student_management"])
    elif "teacher" in msg:
        reply = choice(chat_bot_responses["teacher_management"])
    elif "admin" in msg:
        reply = choice(chat_bot_responses["admin_management"])

    # ATTENDANCE
    elif "attendance" in msg:
        if "student" in msg:
            reply = choice(chat_bot_responses["student_attendance"])
        else:
            reply = choice(chat_bot_responses["attendance_info"])

    # CLASSROOM / SUBJECTS
    elif "classroom" in msg or "class" in msg:
        reply = choice(chat_bot_responses["classroom"])
    elif "subject" in msg:
        reply = choice(chat_bot_responses["subjects"])

    # ASSIGNMENTS
    elif "assignment" in msg:
        if "submit" in msg or "student" in msg:
            reply = choice(chat_bot_responses["assignments_student"])
        else:
            reply = choice(chat_bot_responses["assignments_teacher"])

    # GRADES
    elif "grade" in msg or "grading" in msg:
        if "student" in msg:
            reply = choice(chat_bot_responses["grading_student"])
        else:
            reply = choice(chat_bot_responses["grading_teacher"])

    # FILE UPLOADS
    elif "upload" in msg or "file" in msg or "photo" in msg:
        reply = choice(chat_bot_responses["file_uploads"])

    # TIMETABLE
    elif "timetable" in msg or "schedule" in msg:
        reply = choice(chat_bot_responses["timetable"])

    # ANNOUNCEMENTS
    elif "announcement" in msg or "notice" in msg:
        reply = choice(chat_bot_responses["announcements"])

    # EVENTS
    elif "event" in msg or "holiday" in msg:
        reply = choice(chat_bot_responses["events"])

    # SETTINGS
    elif "settings" in msg or "config" in msg:
        reply = choice(chat_bot_responses["settings"])

    # CMS
    elif "cms" in msg or "system" in msg:
        reply = choice(chat_bot_responses["cms_info"])

    # SUPPORT
    elif "help" in msg or "support" in msg or "issue" in msg:
        reply = choice(chat_bot_responses["support"])

    # ERROR / FALLBACK
    else:
        reply = choice(chat_bot_responses["fallback"])

    return jsonify({"reply": reply})

# -------------------- END CHAT-BOT ----------------------------------------------------------


# -------------------- START PROFILE & SETTINGS ------------------------------------------------




@dash_bp.route("/view_profile", methods=["GET", "POST"])
@role_required("teacher", "admin", "student")
def view_profile():
    from werkzeug.utils import secure_filename
    from werkzeug.security import generate_password_hash
    from auth.models import Teacher, Admin, Student, AvatorFileUpload

    user_profile = None
    profile_record = None
    password_updated = False
    upload_error = None
    upload_success = None

    # Get user and profile record
    if current_user.role == "teacher":
        user_profile = Teacher.query.get_or_404(current_user.id)
        profile_record = user_profile.teacherschoolrecord
        existing_avatar = profile_record.teacher_avator
    elif current_user.role == "admin":
        user_profile = Admin.query.get_or_404(current_user.id)
        profile_record = user_profile.admin
        existing_avatar = profile_record.student_avator
    else:
        user_profile = Student.query.get_or_404(current_user.id)
        profile_record = user_profile.student
        existing_avatar = profile_record.student_avator

    if request.method == "POST":
        # Update password
        new_password = request.form.get("password")
        if new_password:
            user_profile.hashed_password = generate_password_hash(new_password)
            db.session.commit()
            password_updated = True

        # Handle profile picture upload
        if "profile_photo" in request.files:
            file = request.files["profile_photo"]
            if file.filename == "":
                upload_error = "No file selected."
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config["PROFILE_PHOTO_UPLOAD"]
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)

                try:
                    if existing_avatar:
                        # Update existing avatar record
                        existing_avatar.original_name = file.filename
                        existing_avatar.filename = filename
                        existing_avatar.filepath = filepath
                    else:
                        # Create new avatar record
                        new_avatar = AvatorFileUpload(
                            original_name=file.filename,
                            filename=filename,
                            filepath=filepath,
                            teacher_school_record_id=profile_record.id if current_user.role == "teacher" else None,
                            student_school_record_id=profile_record.id if current_user.role != "teacher" else None
                        )
                        db.session.add(new_avatar)

                    db.session.commit()
                    upload_success = "Profile picture updated successfully!"
                except Exception as e:
                    db.session.rollback()
                    upload_error = "Failed to update profile picture."

            else:
                upload_error = "Invalid file type. Allowed: png, jpg, jpeg, gif."

    return render_template(
        "profile/view_profile.html",
        user=user_profile,
        profile_record=profile_record,
        password_updated=password_updated,
        upload_error=upload_error,
        upload_success=upload_success
    )
# -------------------- END PROFILE ------------------------------------------------

# -------------------- START STUDY MATERIAL ------------------------------------------------
# 
@dash_bp.route("/study-material/create", methods=["GET", "POST"])
@role_required("teacher")
def create_study_material():
    from dash.models import StudyMaterial,StudyMaterialFileUpload,Classroom 

    classrooms = Classroom.query.all()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        classroom_id = request.form.get("classroom_id")

        material = StudyMaterial(
            title=title,
            description=description,
            classroom_id=classroom_id,
            teacher_id=current_user.id
        )
        db.session.add(material)
        db.session.commit()

        # File uploads
        files = request.files.getlist("files")
        upload_dir = current_app.config["STUDY_MATERIAL_UPLOAD"]

        for file in files:
            if file.filename:
                filepath = os.path.join(upload_dir, file.filename)
                file.save(filepath)

                db.session.add(
                    StudyMaterialFileUpload(
                        filename=file.filename,
                        filepath=filepath,
                        study_material_id=material.id
                    )
                )

        db.session.commit()

        return redirect(url_for("dash.list_study_material"))

    return render_template("study_material/create.html", classrooms=classrooms)



# LIST + PAGINATION + PER PAGE
@dash_bp.route("/study-material", methods=["GET"])
@login_required
def list_study_material():
    from dash.models import StudyMaterial 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)

    materials = StudyMaterial.query.order_by(
        StudyMaterial.created_at.desc()
    ).paginate(page=page, per_page=per_page)

    return render_template(
        "study_material/list.html",
        materials=materials,
        per_page=per_page
    )

# VIEW ONE
@dash_bp.route("/study-material/<int:id>", methods=["GET"])
@login_required
def view_study_material(id):
    from dash.models import StudyMaterial 
    material = StudyMaterial.query.get_or_404(id)
    return render_template("study_material/view.html", material=material)

# UPDATE (Teacher only)
@dash_bp.route("/study-material/<int:id>/edit", methods=["GET", "POST"])
@role_required("teacher")
def edit_study_material(id):
    from dash.models import StudyMaterial,Classroom 

    material = StudyMaterial.query.get_or_404(id)
    classrooms = Classroom.query.all()

    if request.method == "POST":
        material.title = request.form.get("title")
        material.description = request.form.get("description")
        material.classroom_id = request.form.get("classroom_id")

        db.session.commit()
        return redirect(url_for("dash.view_study_material", id=id))

    return render_template("study_material/edit.html", material=material, classrooms=classrooms)


# DELETE (Teacher only + confirmation)
# GET → show confirm page
@dash_bp.route("/study-material/<int:id>/delete")
@role_required("teacher")
def delete_study_material_confirm(id):
    from dash.models import StudyMaterial
    material = StudyMaterial.query.get_or_404(id)
    return render_template("study_material/delete_confirm.html", material=material)

# POST → delete
@dash_bp.route("/study-material/<int:id>/delete", methods=["POST"])
@role_required("teacher")
def delete_study_material(id):
    from dash.models import StudyMaterial
    material = StudyMaterial.query.get_or_404(id)
    
    # delete file uploads
    for f in material.files:
        if os.path.exists(f.filepath):
            os.remove(f.filepath)

    db.session.delete(material)
    db.session.commit()

    return redirect(url_for("dash.list_study_material"))





# -------------------- END STUDY MATERIAL ------------------------------------------------


# -------------------- START GENERATE REPORTS ------------------------------------------------


# -------------------- END GENERATE REPORTS ------------------------------------------------





