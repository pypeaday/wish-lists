from typing import List, Tuple

import pandas as pd
import starlette.status as status
from fastapi import APIRouter, Depends, Form, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api import api
from app.model.model import Wishes
from app.schema.schema import wish_schema
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


@router.get("/wishes/add", response_class=HTMLResponse)
async def get_add_wishes(request: Request):

    return templates.TemplateResponse(
        "add_wish.html",
        {
            "request": request,
            "data": {},
        },
    )


@router.post("/wishes/add", response_class=HTMLResponse)
async def add_wish(
    name: str = Form(...),
    wish=Form(...),
    link: str = Form(...),
    db: Session = Depends(create_get_session),
):
    new_wish = Wishes(
        person=name,
        item=wish,
        link=link,
        purchased="Not Yet",
    )
    await api.add_wish(
        wish=new_wish,
        db=db,
    )

    return RedirectResponse("/wishes", status_code=status.HTTP_302_FOUND)


@router.get("/wishes/remove", response_class=HTMLResponse)
async def get_remove_wishes(
    request: Request, db: Session = Depends(create_get_session)
):

    data: List[wish_schema] = await api.read_wishes(db)

    return templates.TemplateResponse(
        "remove_wishes.html",
        {
            "request": request,
            "data": data,
        },
    )


@router.post("/wishes/remove", response_class=HTMLResponse)
async def remove_wish(
    request: Request,
    # check1: int = Form(...),
    db: Session = Depends(create_get_session),
):
    form_data = await request.form()
    data = jsonable_encoder(form_data)
    for k, v in data.items():
        await api.delete_wish(
            wish_id=v,
            db=db,
        )

    return RedirectResponse("/wishes", status_code=status.HTTP_302_FOUND)
    # return templates.TemplateResponse(
    #     "remove_wishes.html",
    #     context={
    #         "request": request,
    #         "data": (
    #             Wishes(person="tests", item="only", link="linksy", purchased=False),
    #         ),
    #     },
    # )
