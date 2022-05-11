import time
from typing import Optional

from pydantic import BaseModel


class wish_schema(BaseModel):

    person: str
    item: str
    link: str
    purchased: str = "Not Yet"
    purchased_by: Optional[str] = None
    date_added: Optional[str] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    class Config:
        orm_mode = True


class patch_schema(BaseModel):

    id: int
    purchased: str
    purchased_by: Optional[str] = "Albus Dumbledore"

    class Config:
        orm_mode = True
