import os
import os.path


ICKAFKA_FOLDER = os.path.join(os.path.expanduser("~"), ".ickafka")
CAPTURES_FOLDER = os.path.join(os.path.expanduser("~"), ".ickafka/captures")


def create_config_dir():
    """Creates a folder named .ickafka in user's home directory"""
    if not os.path.isdir(ICKAFKA_FOLDER):
        os.mkdir(ICKAFKA_FOLDER)
    if not os.path.isdir(CAPTURES_FOLDER):
        os.mkdir(CAPTURES_FOLDER)
