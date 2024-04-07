from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/add", summary="add feedback")
async def add_feedback():
    return JSONResponse({"status": "Ok"})


@router.get("/get", summary="get feedback")
async def get_feedback():
    return JSONResponse({"status": "Ok"})


@router.get("/search", summary="search feedback")
async def search_feedback():
    return JSONResponse({"status": "Ok"})