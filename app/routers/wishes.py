from typing import List, Tuple

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

COLUMNS = {
    "id": "key",
    "person": "Name",
    "item": "Wish",
    "link": "Link",
    "purchased": "Purchased",
    "purchased_by": "Purchased By",
    "date_added": "Date Added",
}


def _format_wishes(
    data: List[wish_schema],
) -> Tuple[List[wish_schema], pd.DataFrame, str]:

    rows = [
        [d.id, d.person, d.item, d.link, d.purchased, d.purchased_by, d.date_added]
        for d in data
    ]

    df = pd.DataFrame.from_records(rows, columns=COLUMNS.keys())
    table = (
        df[COLUMNS.keys()]
        .rename(columns=COLUMNS)
        .to_html(index=False, classes=["table table-bordered table-dark table-hover"])
    )

    return df, table


@router.get("/wishes", response_class=HTMLResponse)
async def get_wishes(request: Request, db: Session = Depends(create_get_session)):

    data: List[wish_schema] = await api.read_wishes(db)

    _, table = _format_wishes(data)

    return templates.TemplateResponse(
        "wish.html",
        {
            "request": request,
            "data": {
                "table": table,
                "data": data,
            },
        },
    )


@router.post("/wishes", response_class=HTMLResponse)
async def form_update_wish_form(
    request: Request,
    db: Session = Depends(create_get_session),
    key: str = Form(...),
    person: str = Form(...),
):
    patch = Wishes(id=key, purchased="Yes", purchased_by=person)
    await api.update_wish(patch=patch, db=db)

    data: List[wish_schema] = await api.read_wishes(db)

    _, table = _format_wishes(data)
    return templates.TemplateResponse(
        "wish.html",
        context={
            "request": request,
            "data": {
                "table": table,
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
