import utils.common
import utils.time_tracker
import pandas as pd
import datetime


def this_week():
    df = utils.time_tracker.get_data()
    df["date"] = df["start_time"].dt.date

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    df = df[df["date"] >= start_of_week]

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

    # TODO adapt weekly target and work_days_cnt based on public holidays? if possible, maybe look into personal calendar
    work_days_cnt = 5
    weekly_target = utils.common.read_config()["tt_weekly_target"]
    friday_target_hr = 5

    weekly_time_remaining = round(weekly_target - total, 2)
    daily_values = {
        x[1]["date"]: round(x[1]["duration"] / 3600, 2) for x in daily_df.iterrows()
    }
    projected_daily_avg = (weekly_time_remaining - friday_target_hr) / (
        work_days_cnt - len(daily_values) - 1  # - 1 for friday
    )
    projected_daily_avg = round(projected_daily_avg, 2)

    # TODO once there is a frontend, return time worked for day + if in_progress a timestamp of last start event so we can live update
    response = {
        "total": round(total, 2),
        "daily": daily_values,
        "in_progress": in_progress,
        "percentage": round((total / weekly_target) * 100, 2),
        "weekly_time_remaining": weekly_time_remaining,
        "projected_daily_avg_for_5hr_friday": projected_daily_avg,
    }
    if in_progress:
        response["time_in_progress"] = round(time_in_progress, 2)

    return response
