from app.views import register, login
from flask import Blueprint,make_response,redirect,url_for,flash,request
from app.util import token_required
from app.loggers import ActivityLogger, ErrorLogger
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

error_logger = ErrorLogger()
activity_logger = ActivityLogger()
@auth_bp.route("/")
@auth_bp.route("/auth")
@token_required
def home_auth():
    return "<h1>Hello to welcome auth page</h1>"

@auth_bp.route("/register",methods=['GET', 'POST'])
def registration():
    return register.register_user()

@auth_bp.route("/login", methods=['GET', 'POST'])
def signup():
    return login.login_view()

    
@auth_bp.route('/logout')
@token_required
def logout(current_user):
    try:
        response = make_response(redirect(url_for('home_view')))
        response.delete_cookie("Authorization")
        activity_logger.log_activity(
            user=current_user.email,
            action="Logout successful"
        )
        flash("Logout successfully")
        return response
    except Exception as e:
        error_logger.log_error(f"Logout error: {str(e)}")
        return make_response({"error": "Logout failed"}, 500)