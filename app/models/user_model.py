from app.extensions import sql_db
from sqlalchemy import event
from app.models.option_model import Option
from sqlalchemy.orm import Session

class User(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement=True)
    public_id = sql_db.Column(sql_db.String(1000))
    name = sql_db.Column(sql_db.String(50))
    email = sql_db.Column(sql_db.String(255), unique=True)
    password = sql_db.Column(sql_db.Text)

    def create_default_options(self):
        default_options = [
            {'option_type': 'Light', 'description': ''},
            {'option_type': 'Heavy', 'description': ''},
            {'option_type': 'Med', 'description': ''}
        ]
        
        # Create new options
        for opt in default_options:
            option = Option(
                user_id=self.id,
                option_type=opt['option_type'],
                description=opt['description']
            )
            sql_db.session.add(option)