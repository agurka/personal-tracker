import utils.paydays
import pandas as pd


def all_data():
    path = utils.paydays.get_path_to_data()
    df = pd.read_csv(path)
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index, utc=True).strftime("%Y-%m-%d")

    json_data = {
        "data": [
            {"date": date, "amount": amount}
            for date, amount in zip(df.index, df["amount"])
        ]
    }

    return json_data
