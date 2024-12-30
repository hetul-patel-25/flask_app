from flask import Blueprint
from DropConnect import app
from DropConnect.util import token_required
from DropConnect.views import home
home_bp=Blueprint('home',__name__)

from flask import render_template,redirect,url_for
from DropConnect.services import home_service
from DropConnect.models.option_model import Option
from DropConnect.forms import OptionForm

# @app.route("/",methods=['GET','POST'])
# @token_required
# def home_view(current_user):
#     if current_user:
#        return render_template('index.html',current_user=current_user,form=home_service.home())
#     else:
#         return redirect(url_for('auth.registration'))

@app.route("/", methods=['GET', 'POST'])
@token_required
def home_view(current_user):
    if current_user:
        # Initialize form with user_id
        form = OptionForm(user_id=current_user.id)
        
        # Get options list
        options_list = [option.to_dict() for option in Option.query.filter_by(user_id=current_user.id).all()]

        return render_template('index.html', 
                             current_user=current_user,
                             form=form,  # Pass the initialized form
                             options=options_list)
    return redirect(url_for('auth.registration'))
# @token_required
# def home_view(current_user):
#     if current_user:
#         # breakpoint()
#         form=OptionForm()

#         options_list = [option.to_dict() for option in Option.query.filter_by(user_id=current_user.id).all()]
#         choices = [
#             ('option1', 'Option 1'),
#             ('option2', 'Option 2'), 
#             ('option3', 'Option 3'),
#             ('custom', 'Add Custom Option')
#         ]
#         custom_options = Option.query.filter_by(user_id=current_user.id).all()
#         for option in custom_options:
#             if option.option_type not in ['option1', 'option2', 'option3']:
#                 choices.insert(-1, (option.option_type, option.option_type))
#         form.option_type.choices = choices
#         print("=====================================")
#         print("choices:", choices)
#         print("form.option_type.choices:", form.option_type.choices)
#         print("=====================================")

#         return render_template('index.html', 
#                              current_user=current_user,
#                              form=OptionForm(),
#                              options=options_list)
#     return redirect(url_for('auth.registration'))