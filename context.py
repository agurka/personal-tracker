import utils.common
import os
import json
import time


class Context:
    def __init__(self):
        self._config = self._read_config()
        self._data = {}

    def _read_config(self):
        path = os.path.join(utils.common.get_root_folder(), "config.json")
        with open(path, "r") as f:
            cfg = json.load(f)
        return cfg

    def filepath(self, request_path):
        data_files = self._config.get("data_files")
        mapping = {
            "/money/paydays": "paydays",
            "/time/weekly": "time_tracker",
        }
        return data_files.get(mapping.get(request_path))

    def has_valid_data(self, request_path):
        return self._data.get(request_path, {}).get("timestamp", 0) + 60 * 5 > int(
            time.time()
        )

    def data(self, request_path):
        return self._data.get(request_path).get("data")

    def update_data(self, request_path, data):
        if request_path not in self._data:
            self._data[request_path] = {}
        self._data[request_path]["data"] = data
        self._data[request_path]["timestamp"] = int(time.time())
