from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api import api
from app.model.model import Wishes
from app.schema.schema import patch_schema, wish_schema
from app.session.session import create_get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


# class Wishes(Base):
#     __tablename__ = "Wishes"
#     id = Column(Integer, primary_key=True, index=True)
#     person = Column(String(20))
#     item = Column(Text())
#     link = Column(Text())
#     purchased = Column(Boolean())
#     purchased_by = Column(String(90))
#     date_added = Column(String(15))


@router.get("/wishes", response_class=HTMLResponse)
async def get_wishes(request: Request, db: Session = Depends(create_get_session)):
    data: List[wish_schema] = await api.read_wishes(db)
    columns = {
        "id": "key",
        "person": "Name",
        "item": "Wish",
        "link": "Link",
        "purchased": "Purchased",
        "purchased_by": "Purchased By",
        "date_added": "Date Added",
    }
    rows = [
        [d.id, d.person, d.item, d.link, d.purchased, d.purchased_by, d.date_added]
        for d in data
    ]

    df = pd.DataFrame.from_records(rows, columns=columns.keys())

    return templates.TemplateResponse(
        "wish.html",
        {
            "request": request,
            "data": {
                "table": df[columns.keys()]
                .rename(columns=columns)
                .to_html(
                    index=False, classes=["table table-bordered table-dark table-hover"]
                ),
                "data": data,
            },
        },
    )


@router.post("/wishes", response_class=HTMLResponse)
async def form_chosen_item(
    request: Request,
    db: Session = Depends(create_get_session),
    key: str = Form(...),
    person: str = Form(...),
):
    patch = Wishes(id=key, purchased=True, purchased_by=person)
    await api.update_wish(patch=patch, db=db)

    # do everything again
    data: List[wish_schema] = await api.read_wishes(db)
    columns = {
        "id": "key",
        "person": "Name",
        "item": "Wish",
        "link": "Link",
        "purchased": "Purchased",
        "purchased_by": "Purchased By",
        "date_added": "Date Added",
    }
    rows = [
        [d.id, d.person, d.item, d.link, d.purchased, d.purchased_by, d.date_added]
        for d in data
    ]

    df = pd.DataFrame.from_records(rows, columns=columns.keys())
    return templates.TemplateResponse(
        "wish.html",
        context={
            "request": request,
            "chosen_item": "ITEM",
            "data": {
                "table": df[columns.keys()]
                .rename(columns=columns)
                .to_html(
                    index=False, classes=["table table-bordered table-dark table-hover"]
                ),
                "data": data,
            },
        },
    )


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
