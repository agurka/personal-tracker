from fastapi import FastAPI
from routes import router


app = FastAPI()
app.include_router(router)

# from pprint import pprint
# import datetime


# from components import time_tracker

# pprint(time_tracker.this_week())
