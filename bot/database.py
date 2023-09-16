import datetime
import os

from sqlalchemy import Boolean, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

PSQL_DB_NAME = os.environ.get("PSQL_DB_NAME")
PSQL_USERNAME = os.environ.get("PSQL_USERNAME")
PSQL_PASSWORD = os.environ.get("PSQL_PASSWORD")
PSQL_HOSTNAME = os.environ.get("PSQL_HOSTNAME")
PSQL_PORT = os.environ.get("PSQL_PORT")


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{PSQL_USERNAME}:{PSQL_PASSWORD}@"
    f"{PSQL_HOSTNAME}:{PSQL_PORT}/"
    f"{PSQL_DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
Session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users_usermodel"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    date_joined = Column(DateTime(timezone=True), default=datetime.datetime.utcnow())


class PostModel(Base):
    __tablename__ = "posts_postmodel"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    photo = Column(String)  # Replace with the appropriate image field for your database

    user_id = Column(Integer, ForeignKey("users_usermodel.id"), nullable=False)
    user = relationship("UserModel", backref="posts")

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), default=datetime.datetime.utcnow()
    )


class PostsLikesModel(Base):
    __tablename__ = "posts_postslikesmodel"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts_postmodel.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users_usermodel.id"), nullable=False)

    post = relationship("PostModel", backref="post_likes")
    user = relationship("UserModel", backref="like_posts")
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow())

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uq_post_user"),)
