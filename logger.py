import logging
import os

dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(dir, "logs/app.log")


def get_logger():
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s")
    logger = logging.getLogger(__name__)
    return logger