import utils.common
import os


def get_path_to_data():
    config = utils.common.read_config()
    path_to_data = config["data_files"]["paydays"]
    print(f"{path_to_data = }")
    assert os.path.exists(path_to_data)
    return path_to_data
