from flask import Flask, render_template, redirect, url_for
from extensions import db, migrate, login_manager,socketio
from datetime import timedelta,datetime
import os
from typing import cast
from auth.models import Teacher, Admin, Student
from config import Config
from sqlalchemy import text

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
     # Register your context processor here
    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}
    
    # ----------------------
    # Error handlers
    # ----------------------
    @app.errorhandler(403)
    def action_forbidden_found(error):
        return render_template('errors/not_found_error.html'), 403
    
    @app.errorhandler(403)
    def resource_not_found(error):
        return render_template('errors/forbidden_action.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/internal_server_error.html'), 500
    
    @app.route("/cause500")
    def cause500():
        raise Exception("This is a forced 500 error!")

    # ----------------------
    # DB Configurations
    # ----------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classroom.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    # ----------------------
    # File Uploads
    # ----------------------
    BASE_UPLOAD = os.path.join(os.getcwd(), "uploads")
    ASSIGNMENT_UPLOAD = os.path.join(BASE_UPLOAD, "assignments_uploads")
    PROFILE_PHOTO_UPLOAD = os.path.join(BASE_UPLOAD, "profile_photo")
    STUDENT_SUBMISSION_UPLOAD = os.path.join(BASE_UPLOAD, "assignment_student_submission_files")

    for folder in [BASE_UPLOAD, ASSIGNMENT_UPLOAD, PROFILE_PHOTO_UPLOAD, STUDENT_SUBMISSION_UPLOAD]:
        os.makedirs(folder, exist_ok=True)

    app.config["BASE_UPLOAD"] = BASE_UPLOAD
    app.config["ASSIGNMENT_UPLOAD"] = ASSIGNMENT_UPLOAD
    app.config["PROFILE_PHOTO_UPLOAD"] = PROFILE_PHOTO_UPLOAD
    app.config["STUDENT_SUBMISSION_UPLOAD"] = STUDENT_SUBMISSION_UPLOAD

    # ----------------------
    # Remember Me / Sessions
    # ----------------------
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=5)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=5)

    # ----------------------
    # Init Extensions
    # ----------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app,cors_allowed_origins="*")

    # ----------------------
    # Automatic DB check on startup
    # ----------------------
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("DATABASE CONNECTED")
        except Exception as e:
            print(f"DB ERROR: {e}")
            raise RuntimeError("Database connection failed") from e

    # Redirect unauthenticated users
    login_manager.login_view = cast(str, "login") # type: ignore
    login_manager.login_message = None  # type: ignore # disable flashing text

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("auth.login"))

    # ----------------------
    # Multi-model user loader
    # ----------------------
    @login_manager.user_loader
    def load_user(user_id):
        try:
            model_name, pk = user_id.split(":", 1)
            pk = int(pk)
        except Exception:
            return None

        if model_name == "Teacher":
            return Teacher.query.get(pk)
        if model_name == "Admin":
            return Admin.query.get(pk)
        if model_name == "Student":
            return Student.query.get(pk)

        return None
    
    # @app.route('/favicon.ico')
    # def favicon():
    #     return redirect(url_for('static', filename='assets/favicon/learning.png'))

    # ----------------------
    # Register Models
    # ----------------------
    import dash.models

    # ----------------------
    # Register Blueprints
    # ----------------------
    from auth.views import auth_bp
    from dash.views import dash_bp
    from chat.views import chat_bp
    from legal.views import legal_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(dash_bp, url_prefix="/dash")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(legal_bp, url_prefix="/legal")

    return app
