import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers.user import user_router
# from handlers.user import other_router
from database.database import init_db
from keyboards.menu_commands import set_main_menu 
from services.file_handling import prepare_news
from services.search_photo import prepare_photo


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

    logger.info("Preparing photos")
    photos = prepare_photo('images')
    logger.info('The photos is uploaded. Total photos: %d', len(photos))

    db: dict = init_db()
    dp.workflow_data.update(news=news, photos=photos, db=db)

    await set_main_menu(bot)

    dp.include_router(user_router)
    # dp.include_router(other_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())