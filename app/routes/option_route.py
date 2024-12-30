from flask import Blueprint, render_template, jsonify, request, url_for
from app.forms import OptionForm
from app.models.option_model import Option
from app.extensions.db import sql_db
from app.util import token_required
from sqlalchemy import func
from app.loggers.activity_logger import ActivityLogger
from app.loggers.error_logger import ErrorLogger

options_bp = Blueprint('options', __name__)
activity_logger = ActivityLogger()
error_logger = ErrorLogger()

options_bp = Blueprint('options', __name__)

@options_bp.route('/add-option', methods=['GET', 'POST'])
@token_required
def add_option(current_user):
    # Verify user is authenticated
    if not current_user:
        error_logger.log_error("Unauthorized option access attempt")
        return jsonify({'success': False, 'error': 'Authentication required'}), 401

    # Initialize form and get options list
    form = OptionForm(user_id=current_user.id)
    options_list = [option.to_dict() for option in Option.query.filter_by(user_id=current_user.id).all()]

    # Handle GET request
    if request.method == 'GET':
        return render_template('index.html', 
                             form=form, 
                             current_user=current_user,
                             options=options_list)

    # Handle POST request
    try:
        form = OptionForm(user_id=current_user.id, formdata=request.form)
        option_type = form.option_type.data
        option_id = request.form.get('option_id')
        if option_type == 'custom':
          
            if not form.custom_option.data:
                return jsonify({'success': False, 'error': 'Custom option value required'}), 400

            existing = Option.query.filter(
                Option.user_id == current_user.id,
                func.lower(Option.option_type) == func.lower(form.custom_option.data)
            ).first()
            if existing:
                return jsonify({'success': False, 'error': 'Custom option already exists'}), 400
            option_type = form.custom_option.data
        else:
            existing = Option.query.filter(
                Option.user_id == current_user.id,
                func.lower(Option.option_type) == func.lower(option_type)
            ).first()
            if existing:
                option_id = existing.id


        # Check for duplicates
        if option_id:
            # Update existing
            option = Option.query.get_or_404(option_id)
            if option.user_id != current_user.id:
                error_logger.log_error(f"Unauthorized option update attempt by user {current_user.email}")
                return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            option.description = form.description.data
            activity_logger.log_activity(
                user=current_user.email,
                action="Option updated",
                details=f"Updated option: {option.option_type}"
            )
        else:
            # Create new only for custom options
            option = Option(
                user_id=current_user.id,
                option_type=option_type,
                description=form.description.data
            )
            sql_db.session.add(option)
            activity_logger.log_activity(
                user=current_user.email,
                action="Option created",
                details=f"Created new option: {option_type}"
            )

        sql_db.session.commit()
        return jsonify({
            'success': True,
            'option': option.to_dict()
        })

    except Exception as e:
        sql_db.session.rollback()
        error_logger.log_error(f"Option creation/update error for user {current_user.email}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
@options_bp.route('/delete-option/<int:option_id>', methods=['DELETE'])
@token_required
def delete_option(current_user, option_id):
    try:
        option = Option.query.get_or_404(option_id)
        if option.user_id != current_user.id:
            error_logger.log_error(f"Unauthorized option deletion attempt by user {current_user.email}")
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        option_type = option.option_type  
        sql_db.session.delete(option)
        sql_db.session.commit()
        activity_logger.log_activity(
            user=current_user.email,
            action="Option deleted",
            details=f"Deleted option: {option_type}"
        )
        return jsonify({'success': True})
    except Exception as e:
        sql_db.session.rollback()
        error_logger.log_error(f"Option deletion error for user {current_user.email}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500