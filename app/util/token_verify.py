from flask import request,redirect,url_for,render_template
from functools import wraps 
from app.models.user_model import User
from app import app
import jwt

def token_required(func):
    @wraps(func)
    def decorator_fuction(*args,**kwargs):
        token=request.cookies.get('Authorization')
        if not token:
            return redirect(url_for('auth.registration'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
            return render_template('error/temp.html')

        return func(current_user,*args, **kwargs)
        
    return decorator_fuction

            
