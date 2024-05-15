from aiogram import Bot
from aiogram.types import Message, Contact

from misc import Pg
from misc import logger
from locales import get_message_text
from keyboards import get_contact_keyboard, remove_keyboard


async def help_handler(message: Message, bot: Bot) -> None:
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(get_message_text("help", "us"))


async def start_handler(message: Message, bot: Bot, pg: Pg) -> None:
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        get_message_text("start", "us"),
        reply_markup=get_contact_keyboard()
    )


async def contact_handler(message: Message, bot: Bot, pg: Pg):
    contact: Contact = message.contact
    user_id = message.from_user.id

    pg.update_user_phone(user_id, contact.phone_number)

    rem_key = await message.answer(text=".", reply_markup=remove_keyboard())
    await rem_key.delete()

    await message.answer(
        text=get_message_text(
            msgid="answer_on_response_contact",
            language="us",
            phone_number=contact.phone_number
        ),
    )
