from flask import Flask, render_template, redirect, url_for
from extensions import db, migrate, login_manager, socketio
from datetime import timedelta, datetime
import os, sqlite3
from typing import cast
from auth.models import Teacher, Admin, Student
from config import Config
from sqlalchemy import text, event
from sqlalchemy import inspect,Engine

# Import seed scripts
from seed.create_tables import create_tables
from seed.create_subjects_classes import create_subject_classes
from seed.create_teacher_school_records import create_teacher_school_records
from seed.create_students_school_records import create_student_school_records
from seed.associate_teachers_to_subjects import associate_teachers_to_subjects

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ===================== SQLITE FOREIGN KEYS =====================
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    # ===================== CONTEXT PROCESSOR =====================
    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}

    # ===================== ERROR HANDLERS =====================
    @app.errorhandler(403)
    def action_forbidden_found(error):
        return render_template("errors/not_found_error.html"), 403

    @app.errorhandler(404)
    def resource_not_found(error):
        return render_template("errors/forbidden_action.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/internal_server_error.html"), 500

    @app.route("/cause500")
    def cause500():
        raise Exception("This is a forced 500 error!")

    # ===================== DATABASE CONFIG =====================
    print(os.environ.get("FLASK_ENV"))
    # Check if we are in production
    if os.environ.get("FLASK_ENV") == "production":
        # Use MySQL
        username = Config.DB_USERNAME
        password = Config.DB_PASSWORD
        host = Config.DB_HOST
        port = Config.DB_PORT
        db_name = Config.DB_NAME
        uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
    else:
        # Use SQLite for development
        instance_path = os.path.join(os.getcwd(), "instance")
        os.makedirs(instance_path, exist_ok=True)
        uri = "sqlite:///" + os.path.join(instance_path, "classroom.sqlite3")

    # Apply configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    # ===================== FILE UPLOADS =====================
    BASE_UPLOAD = os.path.join(os.getcwd(), "uploads")
    ASSIGNMENT_UPLOAD = os.path.join(BASE_UPLOAD, "assignments_uploads")
    PROFILE_PHOTO_UPLOAD = os.path.join(BASE_UPLOAD, "profile_photo")
    STUDENT_SUBMISSION_UPLOAD = os.path.join(BASE_UPLOAD, "assignment_student_submission_files")
    STUDY_MATERIAL_UPLOAD = os.path.join(BASE_UPLOAD, "study_material_uploads")

    for folder in [BASE_UPLOAD, ASSIGNMENT_UPLOAD, PROFILE_PHOTO_UPLOAD, STUDENT_SUBMISSION_UPLOAD,STUDY_MATERIAL_UPLOAD]:
        os.makedirs(folder, exist_ok=True)

    app.config["BASE_UPLOAD"] = BASE_UPLOAD
    app.config["ASSIGNMENT_UPLOAD"] = ASSIGNMENT_UPLOAD
    app.config["PROFILE_PHOTO_UPLOAD"] = PROFILE_PHOTO_UPLOAD
    app.config["STUDENT_SUBMISSION_UPLOAD"] = STUDENT_SUBMISSION_UPLOAD
    app.config["STUDY_MATERIAL_UPLOAD"] = STUDY_MATERIAL_UPLOAD    


    # ===================== SESSIONS =====================
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=5)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=5)

    # ===================== INIT EXTENSIONS =====================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # ===================== CHECK DATABASE =====================
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("DATABASE CONNECTED")
        except Exception as e:
            print(f"DB ERROR: {e}")
            raise RuntimeError("Database connection failed") from e

    # ===================== LOGIN MANAGER =====================
    login_manager.login_view = cast(str, "login") # type: ignore
    login_manager.login_message = None # type: ignore

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("auth.login"))

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

    # ===================== LOAD MODELS =====================
    import dash.models  # ensures models load before migrations

    # ===================== BLUEPRINTS =====================
    from auth.views import auth_bp
    from dash.views import dash_bp
    from legal.views import legal_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(dash_bp, url_prefix="/dash")
    app.register_blueprint(legal_bp, url_prefix="/legal")

   

   # ===================== SEED DATA (RUN ONCE) =====================
    # with app.app_context():
    #     inspector = inspect(db.engine)

    #     # --- 1. Create tables only if they do not exist ---
    #     if not inspector.has_table("teacher_school_record"):
    #         print("Creating tables...")
    #         create_tables()
    #         print("Tables created successfully!")
    #     else:
    #         print("Tables already exist. Skipping table creation.")

    #     # --- 2. Create seed_status table if not exists ---
    #     if not inspector.has_table("seed_status"):
    #         db.session.execute(text(
    #             "CREATE TABLE IF NOT EXISTS seed_status (id INTEGER PRIMARY KEY AUTOINCREMENT, seeded BOOLEAN)"
    #         ))
    #         db.session.commit()

    #     # --- 3. Run seed data only once ---
    #     result = db.session.execute(text("SELECT seeded FROM seed_status LIMIT 1")).fetchone()
    #     if not result or not result[0]:
    #         print("Running seed data for the first time...")
    #         try:
    #             create_subject_classes()
    #             create_teacher_school_records()
    #             create_student_school_records()
    #             associate_teachers_to_subjects()
    #             db.session.execute(text("INSERT INTO seed_status (seeded) VALUES (1)"))
    #             db.session.commit()
    #             print("Seed data completed!")
    #         except Exception as e:
    #             db.session.rollback()
    #             print(f"Seed data failed: {e}")
    #     else:
    #         print("Seed data already run. Skipping.")

    # with app.app_context():
    #     try:
    #         print("Running seed data...")
    #         create_tables()
    #         create_subject_classes()
    #         create_teacher_school_records()
    #         create_student_school_records()
    #         associate_teachers_to_subjects()

    #         db.session.commit()
    #         print("Seed data completed successfully!")

    #     except Exception as e:
    #         db.session.rollback()
    #         print(f"Seed data failed: {e}")


    # with app.app_context():
    #     inspector = inspect(db.engine)

    #     if not inspector.has_table("student"):
    #         print("Creating tables...")
    #         db.create_all()
    #         print("Tables created")

    #         print("Running seed data...")
    #         create_subject_classes()
    #         create_teacher_school_records()
    #         create_student_school_records()
    #         associate_teachers_to_subjects()
    #         db.session.commit()
    #         print("Seed complete")
    #     else:
    #         print("Database already seeded. Skipping.")

        

    return app