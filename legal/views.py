from flask import render_template,redirect
from . import legal_bp

@legal_bp.route('/privacy-policy')
def privacy():
    return render_template("legal/privacy_policy.html")

@legal_bp.route('/terms-and-conditions')
def terms():
    return render_template("legal/terms_conditions.html")