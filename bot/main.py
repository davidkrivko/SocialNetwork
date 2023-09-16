import asyncio

from dotenv import load_dotenv
from pathlib import Path
from faker import Faker

load_dotenv()

fake = Faker()
MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"


if __name__ == "__main__":
    from bot.functions import run_bot

    config = {
        "num_of_users": 5,
        "max_posts_per_user": 3,
        "max_likes_per_user": 15,
    }
    asyncio.run(run_bot(config))
