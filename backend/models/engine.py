from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, create_session, DeclarativeBase


class Base(DeclarativeBase):
    pass

class