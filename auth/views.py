from flask import request, jsonify, session,render_template,url_for,redirect
from flask_login import login_user, logout_user,current_user
from extensions import db
from auth.models import TeacherSchoolRecord, StudentSchoolRecord, Teacher, Student, Admin
from werkzeug.security import generate_password_hash
from . import auth_bp

# ---------------------------
# REGISTER USER
# ---------------------------
@auth_bp.route("/register", methods=["POST"])
def register_post():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data submitted"}), 400

    school_id = data.get("school_id")
    password = data.get("password")
    role = data.get("role")

    valid_roles = {"teacher", "admin", "student"}
    if role not in valid_roles:
        return jsonify({"success": False, "message": "Invalid role selected"}), 400

    if not school_id or not password:
        return jsonify({"success": False, "message": "School ID and password are required"}), 400

    school_record = StudentSchoolRecord.get_student_by_card_id(school_id)
    teacher_record = TeacherSchoolRecord.get_teacher_by_card_id(school_id)

    if role == "teacher" and not teacher_record:
        return jsonify({"success": False, "message": f"Teacher with ID {school_id} not found"}), 404
    elif role == "student" and not school_record:
        return jsonify({"success": False, "message": f"Student with ID {school_id} not found"}), 404
    elif role == "admin":
        if not school_record:
            return jsonify({"success": False, "message": f"Admin with ID {school_id} not found"}), 404
        if not school_record.is_admin:
            return jsonify({"success": False, "message": "This user is not allowed to create an admin account"}), 403

    # Check duplicates
    if role == "teacher" and Teacher.query.filter_by(user_card_id=school_id).first():
        return jsonify({"success": False, "message": "Teacher account already exists"}), 409
    if role == "student" and Student.query.filter_by(user_card_id=school_id).first():
        return jsonify({"success": False, "message": "Student account already exists"}), 409
    if role == "admin" and Admin.query.filter_by(user_card_id=school_id).first():
        return jsonify({"success": False, "message": "Admin account already exists"}), 409

    try:
        if role == "teacher":
            user = Teacher(user_card_id=school_id, password=password, role=role,
                           teacher_school_record_id=teacher_record.id)
        elif role == "student":
            user = Student(user_card_id=school_id, password=password, role=role,
                           student_school_record_id=school_record.id)
        else:
            user = Admin(user_card_id=school_id, password=password, role=role,
                         student_school_record_id=school_record.id)

        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "Account created successfully", "redirect": "/"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Failed to register user: {str(e)}"}), 500


# ---------------------------
# LOGIN USER
# ---------------------------
# ============================
# LOGIN PAGE / LOGIN POST
# ============================
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Render the login/register page
        return render_template("auth/index.html")
    
    # POST request → handle login via JSON
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data submitted"}), 400

    school_id = data.get("school_id")
    password = data.get("password")
    role = data.get("role")
    remember = data.get("remember", False)

    if not school_id or not password:
        return jsonify({"success": False, "message": "School ID and password are required"}), 400

    valid_roles = {"teacher", "admin", "student"}
    if role not in valid_roles:
        return jsonify({"success": False, "message": "Invalid role selected"}), 400

    user = None
    if role == "teacher":
        user = Teacher.query.filter_by(user_card_id=school_id).first()
    elif role == "admin":
        user = Admin.query.filter_by(user_card_id=school_id).first()
    else:
        user = Student.query.filter_by(user_card_id=school_id).first()

    if not user:
        return jsonify({"success": False, "message": "Account not found"}), 404

    if not user.check_hashed_password(password):
        return jsonify({"success": False, "message": "Invalid password"}), 401

    login_user(user, remember=remember)
    session.permanent = True

     # Determine redirect based on role
    if role == "student" or (role == "admin" and hasattr(user, "student")):
        # Students & admin who has student record → student dashboard
        dashboard_url = url_for("dash.student_submission_assignments")
    elif role == "teacher":
        dashboard_url = url_for("dash.index")
    else:
        # fallback
        dashboard_url = url_for("dash.index")

    return jsonify({"success": True, "message": "Logged in successfully", "redirect": dashboard_url}), 200


# ---------------------------
# LOGOUT
# ---------------------------
@auth_bp.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated: # type: ignore
        logout_user()
        return jsonify({
            "success": True,
            "message": "Logged out successfully",
            "redirect": url_for("auth.login")
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "You are already logged out",
            "redirect": url_for("auth.login")
        }), 200



# FORGOT PASSWORD

@auth_bp.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    from auth.models import Student, Teacher, Admin

    if request.method=='POST':
        school_id = request.form.get('school_id')
        role = request.form.get('role')

        user = None
        if role=="student": user=Student.query.filter_by(user_card_id=school_id).first()
        elif role=="teacher": user=Teacher.query.filter_by(user_card_id=school_id).first()
        elif role=="admin": user=Admin.query.filter_by(user_card_id=school_id).first()

        if user:
            session['reset_user_id'] = user.id
            session['reset_role'] = role
            return redirect(url_for('auth.create_new_password'))
        else:
            return render_template('auth/forgot_password.html', error="No user found with this School ID and role")

    return render_template('auth/forgot_password.html')

@auth_bp.route('/create_new_password', methods=['GET','POST'])
def create_new_password():
    if 'reset_user_id' not in session or 'reset_role' not in session:
        return redirect(url_for('auth.forgot_password'))

    user_id = session['reset_user_id']
    role = session['reset_role']
    from auth.models import Student, Teacher, Admin

    user_model = {"student": Student, "teacher": Teacher, "admin": Admin}.get(role)
    user = user_model.query.get(user_id)

    if request.method=='POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('auth/create_new_password.html', error="Passwords do not match")

        try:
            # ✅ Update correct field
            user.hashed_password = generate_password_hash(password)
            db.session.commit()
            session.pop('reset_user_id')
            session.pop('reset_role')
            return render_template('auth/create_new_password.html', success="Password updated successfully!")
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('auth/create_new_password.html', error="Failed to update password")

    return render_template('auth/create_new_password.html')


# ---------------------------
# OTHER PAGES (rendered normally)
# ---------------------------


@auth_bp.route("/contact-us")
def contact_us():
    return render_template('auth/contact_us.html')


@auth_bp.route("/services")
def services():
    return render_template('auth/services.html')


@auth_bp.route("/about")
def about():
    return render_template('auth/about.html')
