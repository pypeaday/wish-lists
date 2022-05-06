from pydantic import BaseModel
from typing import Optional


class wish_schema(BaseModel):

    person: str
    item: str
    link: str
    purchased: bool = False
    purchased_by: Optional[str] = None
    date_added: Optional[str] = None

    class Config:
        orm_mode = True
