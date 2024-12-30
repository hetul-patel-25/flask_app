from flask import request,Flask,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from app.models.user_model import User
from app.extensions import sql_db
import uuid
from app.forms import RegistrationForm
from app.loggers.activity_logger import ActivityLogger
from app.loggers.error_logger import ErrorLogger

activity_logger = ActivityLogger()
error_logger = ErrorLogger()

def register_user():
    try:
        current_user=None
        data=request.form
        user_name=data.get('name')
        password=data.get('password')
        email=data.get('email')
        form = RegistrationForm()
        if request.method=="POST" and form.validate_on_submit():
            if User.query.filter_by(email=email).first(): 
                error_logger.log_error(f"Registration failed: Email already exists - {email}")
                flash('Email already exists')
                return redirect(url_for('auth.registration'))
            user=User(name=user_name,password=generate_password_hash(password),email =email,public_id=str(uuid.uuid4()))
            sql_db.session.add(user)
            sql_db.session.flush()
            user.create_default_options()        
            sql_db.session.commit()

            activity_logger.log_activity(
                        user=email,
                        action="Registration successful",
                        details=f"Registration from IP: {request.remote_addr}"
                    )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.signup'))
        
        return render_template('auth/register.html',current_user=current_user,form = form )

    except Exception as e:
        error_logger.log_error(f"Unexpected error during registration: {str(e)}")
        return render_template('error/temp.html')
