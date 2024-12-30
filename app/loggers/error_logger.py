import logging
import os
from datetime import datetime

class ErrorLogger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorLogger, cls).__new__(cls)
            cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        cls._logger = logging.getLogger('error_logger')
        cls._logger.setLevel(logging.ERROR)

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create file handler
        log_file = f'logs/error_{datetime.now().strftime("%Y%m%d")}.log'
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.ERROR)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\nStack Trace:\n%(stack_info)s\n'
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        cls._logger.addHandler(handler)

    def log_error(self, error_message, stack_trace=None):
        self._logger.error(
            error_message,
            stack_info=stack_trace if stack_trace else True
        )