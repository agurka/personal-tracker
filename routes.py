from fastapi import APIRouter
import components.paydays
import components.time_tracker

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello!"}


@router.get("/money/paydays")
async def paydays():
    return components.paydays.all_data()


@router.get("/time/weekly")
async def time_weekly():
    return components.time_tracker.this_week()
