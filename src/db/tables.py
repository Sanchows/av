import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    pass


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class SavedAt:
    # Datetime of saving to db

    # People recommend to use server_default
    saved_at: Mapped[datetime.datetime] = mapped_column(default=utcnow())


class Brand(Base, SavedAt):
    __tablename__ = "brand"

    brand_id = mapped_column(Integer, primary_key=True)
    url: Mapped[str]
    label: Mapped[str]
    # probably it's not necessary field
    count: Mapped[int]


class Model(Base, SavedAt):
    __tablename__ = "model"

    model_id = mapped_column(Integer, primary_key=True)
    label: Mapped[str]
    brand_id = mapped_column(ForeignKey("brand.brand_id"))


class Advert(Base, SavedAt):
    __tablename__ = "advert"

    advert_id = mapped_column(Integer, primary_key=True)
    url: Mapped[str]
    description: Mapped[str | None]
    published_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow()
    )
    refreshed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(default=utcnow())

    phones: Mapped[list["Phone"]] = relationship(
        "Phone", secondary="phone_advert"
    )


class Phone(Base):
    __tablename__ = "phone"

    code = mapped_column(String(8), primary_key=True)
    number = mapped_column(Integer, primary_key=True)

    adverts: Mapped[list["Advert"]] = relationship(
        "Advert", secondary="phone_advert"
    )


class PhoneAdvert(Base):
    __tablename__ = "phone_advert"

    advert_id = mapped_column(
        Integer, ForeignKey("advert.advert_id"), primary_key=True
    )

    code = mapped_column(String(8), primary_key=True)
    number = mapped_column(Integer, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint([code, number], [Phone.code, Phone.number]),
        {},
    )
