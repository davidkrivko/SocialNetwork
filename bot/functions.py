import asyncio
import random

from sqlalchemy import select

from bot.main import fake
from bot.utils import create_user, create_post, download_image, create_like
from bot.database import Session, PostModel


async def create_random_users(num_users):
    """
    Create n users
    """
    user_tasks = []

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()

        user_tasks.append(create_user(
            username,
            email,
            password,
            first_name,
            last_name
        ))

    created_users = await asyncio.gather(*user_tasks)
    return created_users


async def create_random_posts(num_posts, users):
    """
    Create posts for new users
    """
    post_tasks = []

    for user in users:
        posts = random.randint(1, num_posts)
        for _ in range(posts):
            title = fake.sentence()
            content = fake.paragraph()
            user_id = user.id
            post_tasks.append(create_post(user_id, title, content))

    created_posts = await asyncio.gather(*post_tasks)
    return created_posts


async def add_images_to_posts(posts):
    """
    Add images for new posts
    """
    download_tasks = [download_image(post) for post in posts]
    await asyncio.gather(*download_tasks)

    async with Session() as db_session:
        await db_session.commit()


async def create_random_likes(num_likes, users):
    """
    Add likes for created posts
    """
    async with Session() as session:
        posts = await session.execute(select(PostModel))
        posts = [post for post in posts]

        likes_tasks = []
        for user in users:
            likes = random.randint(1, num_likes)
            for _ in range(likes):
                post = random.choice(posts)
                likes_tasks.append(create_like(user.id, post[0].id))

        created_posts = await asyncio.gather(*likes_tasks)
        return created_posts


async def run_bot(config: dict):
    num_users = config["num_of_users"]
    max_posts_per_user = config["max_posts_per_user"]
    max_likes_per_user = config["max_likes_per_user"]

    created_users = await create_random_users(num_users)
    created_posts = await create_random_posts(max_posts_per_user, created_users)
    await add_images_to_posts(created_posts)
    await create_random_likes(max_likes_per_user, created_users)
