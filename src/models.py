from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SqlEnum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class User(db.Model):
   
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    
    followers: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="followed")
    following: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="follower")

class Follower(db.Model):
    
    __tablename__ = 'follower'

    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    follower: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

class Post(db.Model):
    
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class Media(db.Model):
    
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")


class Comment(db.Model):
    
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

   
