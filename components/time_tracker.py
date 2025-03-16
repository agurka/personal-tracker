import utils.common
import utils.time_tracker
import pandas as pd
from pprint import pprint


def get_daily_projection(weekly_target_hr, last_day_target_hr, daily_df):
    # convert to seconds for interoperability
    weekly_target_sec = weekly_target_hr * 3600
    last_day_target_sec = last_day_target_hr * 3600

    # get all work days in the week
    df = utils.time_tracker.working_days()

    # filter out past days
    # today = pd.Timestamp(year=2025, month=3, day=14)
    today = pd.Timestamp.now().to_datetime64()
    daily_df = daily_df[daily_df["date"] < today]
    df = df[df["date"] >= today]

    # use real data for past days, empty (to be calculated) for future
    df = pd.concat([daily_df, df])

    last_working_day = df["date"].max()

    if today > last_working_day:
        return utils.time_tracker.daily_times_str(df)

    # fill in missing days
    total_counted = df["duration"].sum(skipna=True)

    remaining = weekly_target_sec - total_counted
    if today == last_working_day:
        df.loc[df["date"] == last_working_day, "duration"] = remaining
    else:
        # set time for the last day
        df.at[df.index[-1], "duration"] = last_day_target_sec
        remaining -= last_day_target_sec

        empty_values = df["duration"].isna().sum()
        if empty_values:
            value_per_day = remaining / empty_values
            df = df.fillna(value=value_per_day)

    return utils.time_tracker.daily_times_str(df)


def this_week(ctx, request_path):
    if ctx.has_valid_data(request_path):
        return ctx.data(request_path)

    df = utils.time_tracker.get_data(ctx, request_path)
    df = utils.time_tracker.filter_week(df, utils.time_tracker.current_week())

    daily_df = df.groupby("date")["duration"].sum().reset_index()
    daily_times_real = utils.time_tracker.daily_times_str(daily_df)

    time_worked, in_progress, time_since_start = utils.time_tracker.total_time_worked(
        df, daily_df
    )
    time_worked_hr = time_worked / 3600

    # TODO adapt weekly target and work_days_cnt based on public holidays? if possible, maybe look into personal calendar
    work_days_cnt = 5
    weekly_target_hr = ctx.get_config("tt_weekly_target")
    last_day_target_hr = ctx.get_config("last_day_target_hrs")
    weekly_time_remaining = round(weekly_target_hr - time_worked_hr, 2)

    # TODO once there is a frontend, return time worked for day + if in_progress a timestamp of last start event so we can live update
    response = {
        "total_time_worked": round(time_worked_hr, 2),
        "daily_times_real": daily_times_real,
        "in_progress": in_progress,
        "percentage": round((time_worked_hr / weekly_target_hr) * 100, 2),
        "weekly_time_remaining": weekly_time_remaining,
    }

    if in_progress:
        response["time_in_progress"] = round(time_since_start, 2)

    response["daily_times_projected"] = get_daily_projection(
        weekly_target_hr,
        last_day_target_hr,
        daily_df,
    )

    ctx.update_data(request_path, response)
    return response
