import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
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

    saved_at: Mapped[datetime.datetime] = mapped_column(default=utcnow())


class UpdatedAt:
    # Datetime of updating in db

    updated_at: Mapped[datetime.datetime] = mapped_column(default=utcnow())


class Brand(Base, SavedAt):
    __tablename__ = "brand"

    brand_id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    label: Mapped[str]
    # probably it's not necessary field
    count: Mapped[int]


class Model(Base, SavedAt):
    __tablename__ = "model"

    model_id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str]
    brand_id = mapped_column(ForeignKey("brand.brand_id"))


class Advert(Base, SavedAt, UpdatedAt):
    __tablename__ = "advert"

    advert_id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    description: Mapped[str | None]
    published_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow()
    )
    refreshed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    phones: Mapped[list["PhoneAdvert"]] = relationship(back_populates="advert")


class Phone(Base):
    __tablename__ = "phone"

    code = mapped_column(String(8), primary_key=True)
    number: Mapped[int] = mapped_column(primary_key=True)

    adverts: Mapped[list["PhoneAdvert"]] = relationship(back_populates="phone")


class PhoneAdvert(Base, SavedAt, UpdatedAt):
    __tablename__ = "phone_advert"

    advert_id: Mapped[int] = mapped_column(
        ForeignKey("advert.advert_id"), primary_key=True
    )
    code = mapped_column(String(8), primary_key=True)
    number: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint([code, number], [Phone.code, Phone.number]),
        {},
    )

    phone: Mapped["Phone"] = relationship(back_populates="adverts")
    advert: Mapped["Advert"] = relationship(back_populates="phones")
