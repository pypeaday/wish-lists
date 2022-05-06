from database import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Integer, String, Text


class Wishes(Base):
    __tablename__ = "Wishes"
    id = Column(Integer, primary_key=True, index=True)
    person = Column(String(20))
    item = Column(Text())
    link = Column(Text())
    purchased = Column(Boolean())
    purchased_by = Column(String(90))
    date_added = Column(String(15))