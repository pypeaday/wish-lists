from pydantic import BaseModel
import time
from typing import Optional


class wish_schema(BaseModel):

    person: str
    item: str
    link: str
    purchased: bool = False
    purchased_by: Optional[str] = None
    date_added: Optional[str] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    class Config:
        orm_mode = True
