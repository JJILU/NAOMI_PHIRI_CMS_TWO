from . import auth_bp
from flask import (render_template,redirect,
    render_template,
    url_for,flash,
    request,
    jsonify)
from auth.models import (
    TeacherSchoolRecord,
    StudentSchoolRecord,
    Teacher,
    Student,
    Admin)
from extensions import db
from flask_login import login_user,logout_user


@auth_bp.route("/register", methods=["GET", "POST"]) # type: ignore
def register():
    if request.method == "GET":
        return render_template('auth/register.html')
    else:
        data = request.get_json()
        print("registered: ",data)

        # check if data was not submitted
        if not data:
            return jsonify({"error": "No data submitted!"}),400
        

        
        missing_fields = []
        
        # check if correct role is selected
        valid_roles = {"teacher","admin","student"}
        if data.get("role") not in valid_roles:
            print("Invalid role selected")
            return jsonify({"error":"Invalid role selected"}),400

        # check if all id and password are submitted
        if  data.get("role") == "Teacher":
            if not data.get("school_id"):     
                missing_fields.append("teacher id missing")    
            if not data.get("password"):
                missing_fields.append("teacher password missing")    



        if  data.get("role") == "Admin":
            if not data.get("school_id"):     
                missing_fields.append("admin id missing")    
            if not data.get("password"):
                missing_fields.append("admin password missing")     

        if  data.get("role") == "Student":
            if not data.get("school_id"):     
                missing_fields.append("student id missing")    
            if not data.get("password"):
                missing_fields.append("student password missing")            
                       
        # if true contains list of missing fields error messages 
        if missing_fields:
            print(missing_fields)
            return jsonify({"error":missing_fields}),400    
        

        # extract data from request
        school_id = data.get("school_id")
        password = data.get("password")
        role = data.get("role")


        # check if ID is in school records
        valid_user=None
        if role == "teacher":
           valid_user =  TeacherSchoolRecord.get_teacher_by_card_id(school_id)
           if not valid_user:
            print(f"No teacher with school id {school_id} found in school records")
            return jsonify({"error":f"No teacher with school id {school_id} found in school records"}),400
        elif role == "admin":
           print(f"No admin with school id {school_id} found in school records")
           valid_user =  StudentSchoolRecord.get_student_by_card_id(school_id)
           if not valid_user:
            return jsonify({"error":f"No admin with school id {school_id} found in school records"}),400
        else:
           valid_user =  StudentSchoolRecord.get_student_by_card_id(school_id)
           if not valid_user:
            print(f"No student with school id {school_id} found in school records")
            return jsonify({"error":f"No student with school id {school_id} found in school records"}),400

        


        # check if data exists in Teacher,Admin,Student
        if  role == "teacher" and Teacher.query.filter_by(teacher_card_id=school_id).first():
            return jsonify({"error": "Teacher account with this id already exists"}),400
        if  role == "admin" and Admin.query.filter_by(admin_card_id=school_id).first():
            return jsonify({"error": "Admin account with this id already exists"}),400
        if  role == "student" and Student.query.filter_by(student_card_id=school_id).first():
            return jsonify({"error": "Student account with this id already exists"}),400
        

        


        # if record doesn't already exist create a record
        r = None
        if role == "teacher":
            r = Teacher(teacher_card_id=school_id,password=password,role=role) # type: ignore
        elif role == "admin":
            r = Admin(admin_card_id=school_id,password=password,role=role)  # type: ignore
        else:
            r = Student(student_card_id=school_id,password=password,role=role)     # type: ignore

        try:    
            db.session.add(r)    
            db.session.commit()  
            return jsonify({"success":"registered successfully","redirect_url":url_for('auth.login')}),201   # type: ignore
        except Exception as e:
            db.session.rollback()
            print(f"Failed to register user: {str(e)}")
            return jsonify({"error":"failed to register user","redirect_url":url_for('auth.register')}),500
        finally:
            db.session.close()


        
        
        
    


@auth_bp.route("/", methods=["GET", "POST"]) # type: ignore
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    else: 
        data = request.get_json()
        print("registered: ",data)

        # check if data was not submitted
        if not data:
            return jsonify({"error": "No data submitted!"}),400
        

        
        missing_fields = []
        
        # check if correct role is selected
        valid_roles = {"teacher","admin","student"}
        if data.get("role") not in valid_roles:
            return jsonify({"error":"Invalid role selected"}),400

        # check if all id and password are submitted
        if  data.get("role") == "Teacher":
            if not data.get("school_id"):     
                missing_fields.append("teacher id missing")    
            if not data.get("password"):
                missing_fields.append("teacher password missing")    



        if  data.get("role") == "Admin":
            if not data.get("school_id"):     
                missing_fields.append("admin id missing")    
            if not data.get("password"):
                missing_fields.append("admin password missing")     

        if  data.get("role") == "Student":
            if not data.get("school_id"):     
                missing_fields.append("student id missing")    
            if not data.get("password"):
                missing_fields.append("student password missing")            
                       
        # if true contains list of missing fields error messages 
        if missing_fields:
            return jsonify({"error":missing_fields}),400    
        

        # extract data from request
        school_id = data.get("school_id")
        password = data.get("password")
        role = data.get("role")


        # check if ID is in school records
        valid_user=None
        if role == "teacher":
           valid_user =  TeacherSchoolRecord.get_teacher_by_card_id(school_id) # type: ignore
           if not valid_user:
            return jsonify({"error":f"No teacher with school id {school_id} found in school records"}),400
        elif role == "admin":
           valid_user =  StudentSchoolRecord.get_student_by_card_id(school_id)
           if not valid_user:
            return jsonify({"error":f"No admin with school id {school_id} found in school records"}),400
        else:
           valid_user =  StudentSchoolRecord.get_student_by_card_id(school_id)
           if not valid_user:
            return jsonify({"error":f"No student with school id {school_id} found in school records"}),400
           
        # check if data exists in Teacher,Admin,Student & log user in
        if  role == "teacher" and Teacher.query.filter_by(teacher_card_id=school_id).first():
            login_user(Teacher.query.filter_by(teacher_card_id=school_id).first())
            return jsonify({"success":"logged in successfully", "redirect_url":url_for("dash.teacher_home")}),200
        if  role == "admin" and Admin.query.filter_by(admin_card_id=school_id).first():
            login_user(Admin.query.filter_by(admin_card_id=school_id).first())
            return jsonify({"success":"logged in successfully", "redirect_url":url_for("dash.teacher_home")}),200
        if  role == "student" and Student.query.filter_by(student_card_id=school_id).first(): # type: ignore
            login_user(Student.query.filter_by(student_card_id=school_id).first())
            return jsonify({"success":"logged in successfully", "redirect_url":url_for("dash.teacher_home")}),200 



@auth_bp.route('/logout')   # type: ignore
def logout():
    try:
        logout_user()
        # return jsonify({"success":"logged out successfully", "redirect_url":url_for("auth.login")}),200 
        flash('logged out successfully','success')
        return redirect(url_for("auth.login"))
    except Exception as e:
        # return jsonify({"error":f"logged out failed {str(e)}", "redirect_url":url_for("dash.teacher_home")}),500 
        flash(f'logged out failed {str(e)}','success')
        return redirect(url_for("dash.teacher_home"))

    
        
# ============== forgot password ==========
@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template('auth/forgot_password.html')

# ============== contact us ==========
@auth_bp.route("/contact-us")
def contact_us():
    return render_template('auth/contact_us.html')

# ============== services ==========
@auth_bp.route("/services")
def services():
    return render_template('auth/services.html')

# ============== about ==========
@auth_bp.route("/about")
def about():
    return render_template('auth/about.html')

