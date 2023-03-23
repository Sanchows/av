from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import expression


Base = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class SavedUpdatedAt:
    # Datetime of saving to db

    # People recommend to use server_default
    saved_at = Column(DateTime(), server_default=utcnow(), nullable=False)
    updated_at = Column(DateTime(), nullable=True)


class Advert(Base, SavedUpdatedAt):
    __tablename__ = "advert"

    advert_id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    refreshed_at = Column(DateTime(timezone=True), nullable=True)


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
