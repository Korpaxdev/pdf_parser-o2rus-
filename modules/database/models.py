from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    pass


class Block(BaseTable):
    __tablename__ = "blocks"

    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(String)
    data_length: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(100))
    rus_name: Mapped[str] = mapped_column(String, nullable=True)
    length: Mapped[str] = mapped_column(String(30))
    scaling: Mapped[str] = mapped_column(String(30))
    range: Mapped[str] = mapped_column(String(30))
    spn: Mapped[int] = mapped_column(Integer)
