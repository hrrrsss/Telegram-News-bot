from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_favorite_keyboard(*args: int, news: dict) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    titles = [[f for f in v] for v in news.values()]

    for button in sorted(args):
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{button} - {str(*news[button].keys())}", callback_data=str(button)
            )
        )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON["edit_favorite_button"], callback_data="edit_favorite"
        ),
        InlineKeyboardButton(text=LEXICON["cancel"], callback_data="cancel"),
        width=2,
    )
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int, news: dict) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    titles = [[f for f in v] for v in news.values()]

    for button in sorted(args):
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{LEXICON['del']} {button} - {str(*news[button].keys())}",
                callback_data=f"{button}del",
            )
        )
    
    kb_builder.row(InlineKeyboardButton(text=LEXICON["cancel"], callback_data="cancel"))
    return kb_builder.as_markup()