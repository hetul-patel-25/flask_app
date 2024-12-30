from flask import request,render_template,redirect,url_for,session,make_response,flash
from DropConnect.models.user_model import User
from werkzeug.security import check_password_hash
from DropConnect import app
import jwt  
import datetime
from DropConnect.forms import LoginForm
from DropConnect.loggers.activity_logger import ActivityLogger
from DropConnect.loggers.error_logger import ErrorLogger

activity_logger = ActivityLogger()
error_logger = ErrorLogger()

def login_view():
    login_form = LoginForm()
    if request.method=="POST":
        try:
            data=request.form 
            user=User.query.filter_by(email=data.get('email')).first()
            if user is None:
                flash('User not found')
                response = make_response(redirect(url_for('auth.signup')))
                return response
            if check_password_hash(user.password,data.get('password')):
                try:
                     access_token=jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.now()+datetime.timedelta(hours=2)},app.config['SECRET_KEY'],"HS256")
                     response = make_response(redirect(url_for("home_view")))
                     response.headers["Authorization"] = access_token
                     response.set_cookie("Authorization",access_token)
                     flash('Login successful')
                     activity_logger.log_activity(
                        user=user.email,
                        action="Login successful",
                        details=f"Login from IP: {request.remote_addr}"
                    )
                     return response
                except Exception as e:
                    error_logger.log_error(f"Token generation error for user {user.email}: {str(e)}")
                    return make_response(redirect(url_for('auth.signup')))

            else:
                error_logger.log_error(f"Login failed: Incorrect password for user {data.get('email')}")
                flash('Password is incorrect')
                return redirect(url_for('auth.signup'))
        except Exception as e:
            error_logger.log_error(f"Login process error: {str(e)}")
            return render_template('error/temp.html')
    
    return render_template('auth/login.html',form=login_form,current_user=None) 