import pandas as pd


def all_data(ctx, request_path):
    if ctx.has_valid_data(request_path):
        return ctx.data(request_path)

    path = ctx.filepath(request_path)
    df = pd.read_csv(path)
    json_data = df.to_dict(orient="records")

    ctx.update_data(request_path, json_data)
    return json_data
