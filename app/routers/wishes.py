import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import api
from app.model.model import Wishes

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/wishes", response_class=HTMLResponse)
def form_get(request: Request):
    df: pd.DataFrame = api.read_wishes()
    return templates.TemplateResponse(
        "wish.html", context={"request": request, "data": df.to_html()}
    )


@router.get("/wishes", response_class=HTMLResponse)
def add_wish(wish: wish_schema, db: Session = Depends(create_get_session)):
    api.add_wish(
        wish=None,
        db=None,
    )
    new_wish = Wishes(
        person=wish.person,
        item=wish.item,
        link=wish.link,
        purchased=wish.purchased,
        purchased_by=wish.purchased_by,
        date_added=wish.date_added,
    )
    db.add(new_wish)
    db.commit()

    return new_wish
