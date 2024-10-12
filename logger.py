import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
import sys
import traceback
from functools import wraps
import time

class Logger:
    """
    A custom logger class that provides advanced logging functionality with both file and console output.
    """

    def __init__(self, name='TheLibrary', log_level=logging.DEBUG, log_format=None, date_format=None):
        """
        Initialize the Logger instance.

        Args:
            name (str): The name of the logger. Defaults to 'TheLibrary'.
            log_level (int): The logging level. Defaults to logging.DEBUG.
            log_format (str): Custom log format. If None, uses default format.
            date_format (str): Custom date format for logs. If None, uses default format.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.log_format = log_format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.date_format = date_format or '%Y-%m-%d %H:%M:%S'
        self.setup_logging()

    def setup_logging(self):
        """
        Set up the logging configuration, including file and console handlers.
        """
        try:
            # Create asset folder if it doesn't exist
            asset_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
            os.makedirs(asset_folder, exist_ok=True)

            # Set up log file path
            log_file = os.path.join(asset_folder, 'the_library.log')

            # Create a rotating file handler
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )

            # Create a timed rotating file handler (rotates daily)
            timed_handler = TimedRotatingFileHandler(
                log_file,
                when="midnight",
                interval=1,
                backupCount=30
            )

            # Create console handler
            console_handler = logging.StreamHandler()

            # Create formatter and add it to the handlers
            formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
            file_handler.setFormatter(formatter)
            timed_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(timed_handler)
            self.logger.addHandler(console_handler)
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")
            sys.exit(1)

    def _log(self, level, message, exc_info=False, extra=None):
        """
        Internal method to log messages at a specified level.

        Args:
            level (int): The logging level.
            message (str): The message to log.
            exc_info (bool): Whether to include exception information. Defaults to False.
            extra (dict): Extra information to add to the log record.
        """
        try:
            self.logger.log(level, message, exc_info=exc_info, extra=extra)
        except Exception as e:
            print(f"Error logging message: {str(e)}")

    def debug(self, message, extra=None):
        """Log a debug message."""
        self._log(logging.DEBUG, message, extra=extra)

    def info(self, message, extra=None):
        """Log an info message."""
        self._log(logging.INFO, message, extra=extra)

    def warning(self, message, extra=None):
        """Log a warning message."""
        self._log(logging.WARNING, message, extra=extra)

    def error(self, message, extra=None):
        """Log an error message."""
        self._log(logging.ERROR, message, extra=extra)

    def critical(self, message, extra=None):
        """Log a critical message."""
        self._log(logging.CRITICAL, message, extra=extra)

    def exception(self, message, extra=None):
        """Log an exception message with traceback."""
        self._log(logging.ERROR, message, exc_info=True, extra=extra)

    def log_exception(self, exc_type, exc_value, exc_traceback):
        """
        Log an exception with full traceback.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The exception instance.
            exc_traceback (traceback): The traceback object.
        """
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)
        self.error(f"An exception occurred:\n{tb_text}")

    def log_execution_time(self, func):
        """
        Decorator to log the execution time of a function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.debug(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
            return result
        return wrapper

# Create a global logger instance
try:
    logger = Logger()
except Exception as e:
    print(f"Failed to create logger: {str(e)}")
    sys.exit(1)

# Usage example:
if __name__ == "__main__":
    try:
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        
        @logger.log_execution_time
        def slow_function():
            time.sleep(2)
            return "Function completed"

        result = slow_function()
        logger.info(result)

        # Simulate an exception
        1 / 0
    except Exception as e:
        logger.exception("An exception occurred")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.log_exception(exc_type, exc_value, exc_traceback)