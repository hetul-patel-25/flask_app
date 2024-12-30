from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField
from wtforms.validators import DataRequired
from app.models.option_model import Option

class OptionForm(FlaskForm):
    # Define fields first
    option_type = SelectField('Option Type', validators=[DataRequired()])
    custom_option = StringField('Custom Option')
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, user_id=None, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        
        # Initialize default choices
        # choices = [
        #     ('Light', 'Light'),
        #     ('Heavy', 'Heavy'), 
        #     ('Med', 'Med')
        # ]
        choices = []
        # Add user's custom options
        if user_id:
            custom_options = Option.query.filter_by(user_id=user_id).all()
            for option in custom_options:
                # if option.option_type not in ['option1', 'option2', 'option3']:
                choices.insert(-1, (option.option_type, option.option_type))
        
        # Add custom option at end
        choices.append(('custom', 'Add Custom Option'))
        
        # Set choices
        self.option_type.choices = choices