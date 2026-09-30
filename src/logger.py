"""Application logging to data/app.log."""
import logging
import os

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app.log")


def get_logger(name="expense_tracker"):
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.INFO)
        try:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            h = logging.FileHandler(LOG_PATH)
        except OSError:
            h = logging.NullHandler()
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        log.addHandler(h)
    return log
