import logging
import os


class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.configure_logging()

    def configure_logging(self):
        log_path = os.path.join(self.log_dir, "error.log")
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log(self, message):
        logging.info(message)
