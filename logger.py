import logging
import os


class Logger:
    """
    A class for logging messages to a file.

    Attributes:
        log_dir (str): The directory where log files will be stored.
    """

    def __init__(self, log_dir="logs"):
        """
        Initializes the Logger object.

        Args:
            log_dir (str, optional): The directory where log files will be stored. Defaults to "logs".
        """
        self.log_dir = log_dir
        self.create_log_directory()  # ensure log directory and file exist
        self.configure_logging()  # configure the logging system

    def create_log_directory(self):
        """
        Creates the logs directory and error.log file if they do not exist.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)  # create logs directory if it doesn't exist
        error_log_path = os.path.join(self.log_dir, "error.log")
        if not os.path.exists(error_log_path):
            with open(error_log_path, 'w'):
                pass  # create error.log file if it doesn't exist

    def configure_logging(self):
        """
        Configures the logging system.
        """
        log_path = os.path.join(self.log_dir, "error.log")
        logging.basicConfig(
            filename=log_path,  # specify the log file path
            level=logging.DEBUG,  # set the logging level to DEBUG
            format="%(asctime)s - %(levelname)s - %(message)s"  # define the log message format
        )

    def log(self, message):
        """
        Logs a message to the configured log file.

        Args:
            message (str): The message to be logged.
        """
        logging.info(message)  # log the message with INFO level
