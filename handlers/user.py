from copy import deepcopy


from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, FSInputFile, InputMediaPhoto
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.favorite_kb import create_favorite_keyboard
from lexicon.lexicon import LEXICON

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message, db: dict):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in db["users"]:
        db["users"][message.from_user.id] = deepcopy(db.get("user_template"))


@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@user_router.message(Command(commands="beginning"))
async def process_beggining_command(message: Message, news: dict, photos: dict, db: dict):
    db["users"][message.from_user.id]["page"] = 1
    db["users"][message.from_user.id]["img"] = 1
    text = [f'{k}\n\n{v}' for k, v in news[1].items()]
    photo = FSInputFile(photos[1])
    await message.answer_photo(
        photo=photo, 
        caption=text[0], 
        reply_markup=create_pagination_keyboard(
            "backward",
            f"1/{len(news)}",
            "forward",
        ),
    )


@user_router.message(Command(commands="continue"))
async def procces_continue_command(message: Message, news: dict, photos: dict, db: dict):
    text = [f'{k}\n\n{v}' for k, v in news[db["users"][message.from_user.id]["page"]].items()]
    photo = FSInputFile(photos[db["users"][message.from_user.id]["img"]])
    await message.answer_photo(
        photo=photo,
        caption=text[0],
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{db['users'][message.from_user.id]['page']}/{len(news)}",
            "forward",
        ),
    )


@user_router.message(Command(commands="favorite"))
async def procces_favorite_command(message: Message, news: dict, db: dict):
    if db["users"][message.from_user.id]["favorite"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_favorite_keyboard(
                *db["users"][message.from_user.id]["favorite"], news=news
            ),
        )
    else:
        await message.answer(text=LEXICON["no_favorite"])


@user_router.callback_query(F.data == "forward")
async def procces_forward_press(callback: CallbackQuery, news: dict, photos: dict, db: dict):
    current_page = db["users"][callback.from_user.id]["page"]
    if current_page < len(news):
        db["users"][callback.from_user.id]["page"] += 1
        db["users"][callback.from_user.id]["img"] += 1
        photo = FSInputFile(photos[db["users"][callback.from_user.id]["img"]])
        text = [f'{k}\n\n{v}' for k, v in news[db["users"][callback.from_user.id]["page"]].items()]
        media = InputMediaPhoto(media=photo, caption=text[0])
        await callback.message.edit_media(
            media=media,
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{current_page + 1}/{len(news)}",
                "forward",
            )
        )
    await callback.answer()


@user_router.callback_query(F.data == "backward")
async def procces_backward_press(callback: CallbackQuery, news: dict, photos: dict, db: dict):
    current_page = db["users"][callback.from_user.id]["page"]
    if current_page > 1:
        db["users"][callback.from_user.id]["page"] -= 1
        db["users"][callback.from_user.id]["img"] -= 1
        photo = FSInputFile(photos[db["users"][callback.from_user.id]["img"]])
        text = [f'{k}\n\n{v}' for k, v in news[db["users"][callback.from_user.id]["page"]].items()]
        media = InputMediaPhoto(media=photo, caption=text[0])
        await callback.message.edit_media(
            media=media,
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{current_page - 1}/{len(news)}",
                "forward",
            )
        )
        await callback.answer()


@user_router.callback_query(
    lambda x: "/" in x.data and x.data.replace("/", "").isdigit()
)
async def proccess_page_press(callback: CallbackQuery, db: dict):
    db["users"][callback.from_user.id]["favorite"].add(
        db["users"][callback.from_user.id]["page"]
    )
    await callback.answer("Новость добавлена в избранные!")