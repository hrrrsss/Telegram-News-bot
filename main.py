import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from services.file_handling import prepare_news


logger = logging.getLogger(__name__)


async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )
    logger.info("Starting bot")


    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    logger.info("Preparing news")
    news = prepare_news('text_news/news.txt')
    logger.info('The news is uploaded. Total news: %d', len(news))