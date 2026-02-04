from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings

print("IMPORTING base.py")

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"],
)
@base_router.get("/")
async def WelcomeMessage(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "message": f"IT's Team 35 \n Welcome to Our {app_name} Version {app_version}!"
    }