from flask import Blueprint

dash_bp = Blueprint(
    "dash", __name__, template_folder="templates", static_folder="static")

from . import views