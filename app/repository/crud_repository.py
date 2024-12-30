from app.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template,redirect,url_for,flash


class CrudRepository:
    def __init__(self, model):
        self.model = model

    def create(self, data):
        try:
            new_record = self.model(**data)
            sql_db.session.add(new_record)
            sql_db.session.commit()
            return new_record
        except SQLAlchemyError as e:
            print(e)

    def destroy(self, id):
            record = self.get_data(id)
            if not record:
                flash('Record not found', 'error')
                return redirect(url_for('homeroute')) 
            try:
                
                    response=sql_db.session.delete(record)
                    sql_db.session.commit()
                    return response
            except SQLAlchemyError as e:
                sql_db.session.rollback()
                flash('Unable to delete resource', 'error')
                return redirect(url_for('homeroute')) 

    def get_data(self, id):
        record = self.model.query.get(id)

        if not record:
            return redirect(url_for('homeroute')) 
        return record

    def get_all(self):
        data=self.model.query.all()
        return data

    def update(self, id, data):
        try:
                record = self.model.query.get(id)
                for key, value in data.items():
                     setattr(record, key, value)
                sql_db.session.commit()
        
        except SQLAlchemyError as e:
            print("error=======================================")
            print(e)
            sql_db.session.rollback()
            flash('Unable to update resource', 'error')
            return redirect(url_for('homeroute')) 

