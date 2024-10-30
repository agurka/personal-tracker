import utils.common
import os
import pandas as pd


def get_data():
    path = get_path_to_data()
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    starts = df[df["kind"] == "start"].reset_index(drop=True)
    ends = df[df["kind"] == "end"].reset_index(drop=True)
    df = pd.DataFrame(
        {"start_time": starts["timestamp"], "end_time": ends["timestamp"]}
    )
    df["duration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()
    return df


def get_path_to_data():
    config = utils.common.read_config()
    path_to_data = config["data_files"]["time_tracker"]
    assert os.path.exists(path_to_data)
    return path_to_data
