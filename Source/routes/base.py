from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"],
)
@base_router.get("/")
async def WelcomeMessage():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message": f"IT's Team 35 \n Welcome to Our {app_name} Version {app_version}!"
    }