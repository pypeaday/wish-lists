import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# why is this None? / and . both didn't load .env right
load_dotenv(dotenv_path=None)

templates = Jinja2Templates(directory="templates")

router = APIRouter()


# notice this is @router instead of @app
@router.get("/unsplash", response_class=HTMLResponse)
async def unsplash_home(request: Request):
    key = os.getenv("unsplash_key")
    print(key)

    return templates.TemplateResponse("unsplash.html", {"request": request})
