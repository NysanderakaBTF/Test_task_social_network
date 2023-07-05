from sqlalchemy import Column, BigInteger, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from core.db.db_config import Base


class Reaction(Base):
    __tablename__ = 'reactions'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    is_like = Column(Boolean, default=True)

    user = relationship("User", back_populates="reacted_posts_association")
    post = relationship("Post", back_populates="reacted_by_association")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='user_post_rating'),
    )
