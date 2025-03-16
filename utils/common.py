import os


def get_root_folder():
    return os.path.abspath(os.path.join(__file__, "..", ".."))
