from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from locales import get_button_text


def remove_keyboard():
    return ReplyKeyboardRemove()


def get_contact_keyboard():
    contact_request_button = KeyboardButton(
        text=get_button_text("contact_request", "us"),
        request_contact=True
    )
    contact_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [contact_request_button]
        ]
    )

    return contact_keyboard
