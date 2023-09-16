import os

import aiofiles
import aiohttp
from sqlalchemy import update

from bot.database import Session, UserModel, PostModel, PostsLikesModel
from bot.main import MEDIA_DIR, fake
from posts.file_path import custom_upload_path


async def create_user(username, email, password, first_name, last_name):
    """
    Make one user instance
    """
    async with Session() as session:
        user = UserModel(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.commit()
        return user


async def download_image(post):
    """
    Download image for post
    """
    image_url = fake.image_url()
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                relative_path = custom_upload_path(post, f"{fake.word()}.png")
                full_path = os.path.join(MEDIA_DIR, relative_path)

                async with aiofiles.open(full_path, mode="wb") as f:
                    async for chunk in response.content.iter_any():
                        await f.write(chunk)

    stmt = update(PostModel).where(PostModel.id == post.id).values(photo=relative_path)
    async with Session() as session:
        await session.execute(stmt)
        await session.commit()


async def create_post(user_id, title, content):
    """
    Create one post
    """
    async with Session() as session:
        post = PostModel(
            user_id=user_id,
            title=title,
            content=content,
        )
        session.add(post)
        await session.commit()
        return post


async def create_like(user_id, post_id):
    """
    Add like to post
    """
    async with Session() as session:
        like = PostsLikesModel(
            user_id=user_id,
            post_id=post_id,
        )
        try:
            session.add(like)
            await session.commit()
        except:
            pass
        return like
