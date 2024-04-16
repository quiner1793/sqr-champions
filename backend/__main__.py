import uvicorn
from fastapi import FastAPI
from backend.config import config
from backend.entrypoint.auth import router as auth_router
from backend.entrypoint.thread.thread import router as thread_router
from backend.entrypoint.thread.feedback import router as feedback_router
from backend.sources import add_source_events
from backend.utils.auth import router as token_router
from backend.entrypoint.user import router as user_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(token_router)
thread_router.include_router(feedback_router, prefix="/feedback")
app.include_router(thread_router, prefix="/thread")

app.include_router(user_router, prefix="/user")


add_source_events(app, config)

if __name__ == "__main__":
    uvicorn.run("backend.__main__:app",
                host=config.server_host,
                port=config.server_port,
                reload=True)
