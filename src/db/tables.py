from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    pass


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class SavedUpdatedAt:
    # Datetime of saving to db

    # People recommend to use server_default
    saved_at = Column(DateTime(), default=utcnow(), nullable=False)


class Advert(Base, SavedUpdatedAt):
    __tablename__ = "advert"

    advert_id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    refreshed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(), default=utcnow(), nullable=False)

    phones = relationship(
        "Phone", secondary="phone_advert",
    )


class Brand(Base, SavedUpdatedAt):
    __tablename__ = "brand"

    brand_id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    # probably it's not necessary field
    count = Column(Integer)


class Model(Base, SavedUpdatedAt):
    __tablename__ = "model"

    model_id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=True)
    brand_id = Column(Integer, ForeignKey(Brand.brand_id))


class Phone(Base):
    __tablename__ = "phone"

    code = Column(String(8), primary_key=True)
    number = Column(Integer, primary_key=True)

    adverts = relationship(
        "Advert", secondary="phone_advert", back_populates="phones",
    )


class PhoneAdvert(Base):
    __tablename__ = "phone_advert"

    advert_id = Column(
        Integer, ForeignKey("advert.advert_id"), primary_key=True
    )

    code = Column(Integer, ForeignKey("phone.code"), primary_key=True)
    number = Column(Integer, ForeignKey("phone.number"), primary_key=True)
