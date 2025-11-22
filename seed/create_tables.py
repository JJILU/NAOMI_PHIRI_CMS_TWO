from dash.models import compulsarysubject_class,CompulsarySubject,OptionalSubject,Classroom
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("tables created successfully!")
    except Exception as e:
        print(f"Error occured {e}")    