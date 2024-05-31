from aiogram import Router, types, F

from .basic import (
    start_handler,
    help_handler,
    contact_handler
)
from .join import join_handler
from filters.basic import start_command, help_command


def get_user_router() -> Router:
    userRouter = Router()
    userRouter.message.register(start_handler, start_command)
    userRouter.message.register(help_handler, help_command)
    userRouter.message.register(contact_handler, F.contact)

    userRouter.chat_join_request(join_handler)

    return userRouter
