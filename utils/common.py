import os
import json


def read_config():
    path = os.path.join(get_root_folder(), "config.json")
    with open(path, "r") as f:
        cfg = json.load(f)
    return cfg


def get_root_folder():
    return os.path.abspath(os.path.join(__file__, "..", ".."))
