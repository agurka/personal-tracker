import utils.common
import utils.time_tracker
import pandas as pd
from pprint import pprint
import datetime


def this_week():
    df = utils.time_tracker.get_data()
    df["date"] = df["start_time"].dt.date

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    df = df[df["date"] > start_of_week]

    in_progress = pd.isnull(df.iloc[-1]["end_time"])

    if in_progress:
        start_time_today = df.iloc[-1]["start_time"]

    daily_df = df.groupby("date")["duration"].sum().reset_index()
    daily_df.columns = ["date", "duration"]

    daily_df.set_index("date")
    daily_df["day_str"] = pd.to_datetime(daily_df["date"]).dt.strftime("%a")

    total = float(daily_df["duration"].sum() / 3600)

    if in_progress:
        seconds = (
            datetime.datetime.now(tz=datetime.timezone.utc) - start_time_today
        ).total_seconds()
        time_in_progress = seconds / 3600

        total += time_in_progress

    weekly_target = utils.common.read_config()["tt_weekly_target"]
    # TODO once there is a frontend, return time worked for day + if in_progress a timestamp of last start event so we can live update
    response = {
        "total": round(total, 2),
        "daily": {
            x[1]["date"]: round(x[1]["duration"] / 3600, 2) for x in daily_df.iterrows()
        },
        "in_progress": in_progress,
        "percentage": round((total / weekly_target) * 100, 2),
    }
    if in_progress:
        response["time_in_progress"] = round(time_in_progress, 2)

    return response
