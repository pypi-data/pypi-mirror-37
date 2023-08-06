import subprocess
import os
import re


def _exec(command):
    subprocess.call(command.split())


def move_to_lower(filepaths):
    for filepath in filepaths:
        extension = filepath.split('.')[-1]
        if extension.islower():
            continue
        if not os.path.exists(filepath):
            continue
        next_filepath = '{}.{}'.format(
            filepath[:filepath.rfind(".")], extension.lower()
        )
        command = "mv {} {}".format(filepath, next_filepath)
        _exec(command)


def get_image_filepaths(directory_path):
    image_extension_pattern = re.compile(
        r'([jJ][pP][eE]?[gG])|([pP][nN][gG])')
    filepaths = []
    for filename in os.listdir(directory_path):
        extension = filename.split('.')[-1]
        if image_extension_pattern.match(extension):
            filepaths.append(
                os.path.join(os.path.abspath(directory_path), filename))
    return filepaths
