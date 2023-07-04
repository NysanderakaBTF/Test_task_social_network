from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from core.db.db_config import Base
from core.db.mixins.timestamp import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner", cascade='all, delete')

    reacted_posts_association = relationship("Reaction", back_populates="user", cascade='all, delete')
    reacted = relationship("Post", back_populates='reacted_by', secondary='reactions')