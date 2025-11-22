from flask import Flask,render_template
from extensions import db,migrate


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
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///classflow.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init extensions
    db.init_app(app)
    migrate.init_app(app,db)

    # REGISTER MODELS IN CORRECT ORDER
    # import auth.models
    import dash.models


    # import and register blueprints
    from dash.views import dash_bp
    # from auth.views import auth_bp

    # app.register_blueprint(auth_bp,url_prefix="/")
    app.register_blueprint(dash_bp,url_prefix="/dash")

    return app




