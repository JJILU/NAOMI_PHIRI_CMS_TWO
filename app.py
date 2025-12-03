from flask import Flask,render_template
from extensions import db,migrate
from datetime import timedelta
import os


def create_app():
    app = Flask(__name__,template_folder="templates",static_folder="static")

    # 404 error handler
    @app.errorhandler(404)
    def resource_not_found(error):
        return render_template('errors/not_found_error.html')
    
    # 500 error handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/internal_server_error.html')
    
    # raise a 500 error
    @app.route("/cause500")
    def cause500():
        raise Exception("This is a forced 500 error!")


    # app configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///classroom.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # app configurations file uploads
    BASE_UPLOAD = os.path.join(os.getcwd(), "uploads")
    ASSIGNMENT_UPLOAD = os.path.join(BASE_UPLOAD, "assignments_uploads")
    PROFILE_PHOTO_UPLOAD = os.path.join(BASE_UPLOAD, "profile_photo")
    STUDENT_SUBMISSION_UPLOAD = os.path.join(BASE_UPLOAD, "assignment_student_submission_files")

    # Create folders if not exist
    for folder in [BASE_UPLOAD, ASSIGNMENT_UPLOAD, PROFILE_PHOTO_UPLOAD, STUDENT_SUBMISSION_UPLOAD]:
        os.makedirs(folder, exist_ok=True)

    # Add to Flask config
    app.config["BASE_UPLOAD"] = BASE_UPLOAD
    app.config["ASSIGNMENT_UPLOAD"] = ASSIGNMENT_UPLOAD
    app.config["PROFILE_PHOTO_UPLOAD"] = PROFILE_PHOTO_UPLOAD
    app.config["STUDENT_SUBMISSION_UPLOAD"] = STUDENT_SUBMISSION_UPLOAD    

    # enforce max 5 day login 
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=5)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=5)

    # init extensions
    db.init_app(app)
    migrate.init_app(app,db)

    # REGISTER MODELS IN CORRECT ORDER
    # import auth.models
    import dash.models


    # import and register blueprints
    from auth.views import auth_bp
    from dash.views import dash_bp
    from legal.views import legal_bp
    

    app.register_blueprint(auth_bp,url_prefix="/")
    app.register_blueprint(dash_bp,url_prefix="/dash")
    app.register_blueprint(legal_bp,url_prefix="/legal")

    return app




