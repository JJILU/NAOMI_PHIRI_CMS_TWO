from flask import Flask
from extensions import db,migrate


def create_app():
    app = Flask(__name__,template_folder="templates",static_folder="static")

    # app configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///classflow.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init extensions
    db.init_app(app)
    migrate.init_app(app,db)


    # import and register blueprints
    from dash.views import dash_bp
    from auth.views import auth_bp

    app.register_blueprint(auth_bp,url_prefix="/")
    app.register_blueprint(dash_bp,url_prefix="/dash")

    return app




