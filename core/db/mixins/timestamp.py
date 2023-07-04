from sqlalchemy import DateTime, Column, func
from sqlalchemy.orm import declared_attr


class TimestampMixin:

    @declared_attr
    def created_at(cls):
        return Column(DateTime, nullable=False, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())