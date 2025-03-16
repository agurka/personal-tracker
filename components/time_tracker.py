import utils.common
import utils.time_tracker
import pandas as pd
import datetime


def get_daily_projection(
    weekly_target_hr, work_days_cnt, last_day_target_hr, daily_times_real
):
    today = datetime.datetime.now().date()
    before_today = {
        date: time for date, time in daily_times_real.items() if date < today
    }

    total_worked = sum(before_today.values())
    remaining_time = weekly_target_hr - total_worked

    remaining_days_cnt = work_days_cnt - len(before_today)

    daily_projection = {**before_today}

    remaining_days = [
        today + datetime.timedelta(days=i) for i in range(remaining_days_cnt)
    ]
    if remaining_days_cnt == 1:
        val = weekly_target_hr - sum(daily_projection.values())
        daily_projection[remaining_days[0]] = round(val, 2)
    else:
        remaining_time_daily = (remaining_time - last_day_target_hr) / (
            len(remaining_days) - 1
        )
        remaining_time_daily = round(remaining_time_daily, 2)
        for date in remaining_days:
            if date == remaining_days[-1]:
                daily_projection[date] = last_day_target_hr
            else:
                daily_projection[date] = remaining_time_daily
    return daily_projection


def this_week():
    df = utils.time_tracker.get_data()
    df["date"] = df["start_time"].dt.date

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    df = df[df["date"] >= start_of_week]

    # print(df)

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
    weekly_target_hr = utils.common.read_config()["tt_weekly_target"]
    last_day_target_hr = 6

    weekly_time_remaining = round(weekly_target_hr - total, 2)
    daily_times_real = {
        x[1]["date"]: round(x[1]["duration"] / 3600, 2) for x in daily_df.iterrows()
    }

    # TODO once there is a frontend, return time worked for day + if in_progress a timestamp of last start event so we can live update
    response = {
        "total": round(total, 2),
        "daily_times_real": daily_times_real,
        "in_progress": in_progress,
        "percentage": round((total / weekly_target_hr) * 100, 2),
        "weekly_time_remaining": weekly_time_remaining,
    }

    if in_progress:
        response["time_in_progress"] = round(time_in_progress, 2)

    response["daily_times_projected"] = get_daily_projection(
        weekly_target_hr, work_days_cnt, last_day_target_hr, daily_times_real
    )

    return response
