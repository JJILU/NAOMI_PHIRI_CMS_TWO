from app import create_app, socketio

app = create_app()

# This file is only for production (Gunicorn will run this)
