import os
from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=os.environ.get("BOT_TOKEN"),
            admin_ids=list(map(int, os.environ.get('ID_ADMINS').split(',')))
        ),
        db=DbConfig(
            host=os.environ.get('POSTGRES_SERVER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            user=os.environ.get('POSTGRES_USER'),
            database=os.environ.get('POSTGRES_DB')
        ),
        misc=Miscellaneous()
    )
