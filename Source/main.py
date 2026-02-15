"""
this our Rag applicaition for CS-810 course at University of Queen's in Canada. The main.py file is the entry point of our application where we initialize the FastAPI app, set up database connections, and include our route handlers for different endpoints.

Team Members:
1. Nematalla, Esraa - 20592811
2. Elkhuribi, Osama - 20596292   

Date: 2026-02-04

"""
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(base.base_router)
app.include_router(data.data_router)





