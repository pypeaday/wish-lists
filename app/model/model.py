from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

from app.database.database import Base


class Wishes(Base):
    __tablename__ = "Wishes"
    id = Column(Integer, primary_key=True, index=True)
    person = Column(String(20))
    item = Column(Text())
    link = Column(Text())
    purchased = Column(String(10))
    purchased_by = Column(String(90))
    date_added = Column(String(15))
