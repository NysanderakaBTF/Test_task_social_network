from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from core.db.db_config import Base
from core.db.mixins.timestamp import TimestampMixin

class Post(Base, TimestampMixin):
    __tablename__ = 'posts'
    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    owner = relationship('User', back_populates='posts')

    reacted_by_association = relationship("Reaction", back_populates="post", cascade='all, delete')
    reacted_by = relationship("User", back_populates="reacted", secondary='reactions')
