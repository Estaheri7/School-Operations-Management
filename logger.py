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
        self.configure_logging()

    def configure_logging(self):
        """
        Configures the logging system.
        """
        log_path = os.path.join(self.log_dir, "error.log")
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log(self, message):
        """
        Logs a message to the configured log file.

        Args:
            message (str): The message to be logged.
        """
        logging.info(message)
