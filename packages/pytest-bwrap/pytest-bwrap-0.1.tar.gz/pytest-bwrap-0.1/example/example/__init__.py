import pathlib

import requests


def get_gnome():
    return requests.get('https://www.gnome.org')


def write_to_file(path, text):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
