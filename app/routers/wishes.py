from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api import api
from app.schema.schema import wish_schema
from app.session.session import create_get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/wishes", response_class=HTMLResponse)
def get_wishes(request: Request, db: Session = Depends(create_get_session)):
    data: List[wish_schema] = api.read_wishes(db)
    print("data is:\n ", data)
    return templates.TemplateResponse("wish.html", {"request": request, "data": data})


# @router.post("/wishes", response_class=HTMLResponse)
# def add_wish(wish: wish_schema, db: Session = Depends(create_get_session)):
#     api.add_wish(
#         wish=None,
#         db=None,
#     )
#     new_wish = Wishes(
#         person=wish.person,
#         item=wish.item,
#         link=wish.link,
#         purchased=wish.purchased,
#         purchased_by=wish.purchased_by,
#         date_added=wish.date_added,
#     )
#     db.add(new_wish)
#     db.commit()

#     return new_wish
