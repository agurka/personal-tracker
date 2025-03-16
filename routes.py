from fastapi import APIRouter, Request
import context
import components.paydays
import components.time_tracker

router = APIRouter()
ctx = context.Context()


@router.get("/")
async def root():
    return {"message": "Hello!"}


@router.get("/money/paydays")
async def paydays(request: Request):
    return components.paydays.all_data(ctx, request.url.path)


@router.get("/time/weekly")
async def time_weekly(request: Request):
    return components.time_tracker.this_week(ctx, request.url.path)
