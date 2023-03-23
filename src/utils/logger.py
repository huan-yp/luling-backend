import logging
import datetime
import os

from logging import INFO, ERROR, DEBUG


def make_log_path(path):
    os.makedirs(os.path.dirname(path))
    with open(console_log_path, "w+") as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '\n')
        

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logger = logging.Logger("console_logger")
console_log_path = f"./log/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}/console.txt"
make_log_path(console_log_path)
std_handler = logging.StreamHandler()
std_handler.setLevel(INFO)
std_handler.setFormatter(logging.Formatter(LOG_FORMAT))
file_handler = logging.FileHandler(console_log_path, encoding="utf-8")
file_handler.setLevel(DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)
logger.addHandler(std_handler)