import logging
import os
from datetime import datetime

class ActivityLogger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActivityLogger, cls).__new__(cls)
            cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        cls._logger = logging.getLogger('activity_logger')
        cls._logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create file handler
        log_file = f'logs/user_activity_{datetime.now().strftime("%Y%m%d")}.log'
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - User:[%(user)s] - %(message)s'
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        cls._logger.addHandler(handler)

    def log_activity(self, user, action, details=None):
        extra = {'user': user}
        message = f"Action: {action}"
        if details:
            message += f" - Details: {details}"
        self._logger.info(message, extra=extra)