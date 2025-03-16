import pandas as pd


def daily_times_str(df):
    new_df = pd.DataFrame()
    new_df["date"] = df["date"].dt.strftime("%a")
    new_df["duration"] = round(df["duration"] / 3600, 2)

    return {row["date"]: row["duration"] for _, row in new_df.iterrows()}


def total_time_worked(df, grouped_df):
    in_progress = pd.isnull(df.iloc[-1]["end_time"])
    total_time = float(grouped_df["duration"].sum())

    time_since_start = None
    if in_progress:
        time_since_start = (
            pd.Timestamp.now("Europe/Prague") - df.iloc[-1]["start_time"]
        ).total_seconds()
        total_time += time_since_start

    return total_time, in_progress, time_since_start


def working_days():
    today = pd.Timestamp.today("Europe/Prague")
    weekday = today.isocalendar().weekday
    start_of_week = today - pd.Timedelta(days=weekday - 1)
    days = pd.DataFrame({"date": pd.date_range(start_of_week, periods=5, freq="D")})

    days["date"] = days["date"].dt.date
    days["date"] = pd.to_datetime(days["date"])
    return days


def current_week():
    today = pd.Timestamp.today("Europe/Prague")
    # today = pd.Timestamp(year=2024, month=11, day=8)
    iso = today.isocalendar()
    return f"{iso.year}-{iso.week:02d}"


def filter_week(df, week):
    df["isoweek"] = df["start_time"].dt.isocalendar().week
    df["isoyear"] = df["start_time"].dt.isocalendar().year
    df["week"] = df.apply(lambda row: f"{row['isoyear']}-{row['isoweek']}", axis=1)

    df = df[df["week"] == week]
    df = df.drop(columns=["isoweek", "isoyear", "week"])

    df["date"] = df["start_time"].dt.date
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_data(ctx, request_path):
    path = ctx.filepath(request_path)
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    starts = df[df["kind"] == "start"].reset_index(drop=True)
    ends = df[df["kind"] == "end"].reset_index(drop=True)
    df = pd.DataFrame(
        {"start_time": starts["timestamp"], "end_time": ends["timestamp"]}
    )
    df["duration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()
    return df
