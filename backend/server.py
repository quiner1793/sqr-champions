from fastapi import FastAPI
from config import config
from entrypoint.auth import router as auth_router
from entrypoint.feedback import router as feedback_router
from sources import add_source_events


app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(feedback_router, prefix="/feedback")


add_source_events(app, config)
