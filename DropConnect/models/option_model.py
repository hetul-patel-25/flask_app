from DropConnect.extensions.db import sql_db

class Option(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    user_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('user.id'), nullable=False)
    option_type = sql_db.Column(sql_db.String(100), nullable=False)
    description = sql_db.Column(sql_db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'option_type': self.option_type,
            'description': self.description,
            'user_id': self.user_id
        }