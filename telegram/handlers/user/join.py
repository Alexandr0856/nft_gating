from aiogram import Bot
from aiogram.types import ChatJoinRequest

from misc import Pg
from misc import logger
from blockchain.ton_tools import TonTools
from locales import get_message_text


async def join_handler(chat_join_request: ChatJoinRequest, bot: Bot, pg: Pg) -> None:
    logger.info(f"User {chat_join_request.from_user.id} joined chat {chat_join_request.chat.id}")

    user_id = chat_join_request.from_user.id
    chat_id = chat_join_request.chat.id

    user_wallet = pg.get_wallet_address_by_user_id(user_id)

    if user_wallet is not None:
        bc_tools = TonTools()
        await bc_tools.init_tonlib()

        assets = await bc_tools.get_assets_from_wallet(user_wallet)
        if assets is not None:
            chat_nft_collection = pg.get_nft_collection_by_group(chat_id)
            if chat_nft_collection is not None:
                # Check if user has nft of this collection
                if any([asset["contract_address"] == chat_nft_collection for asset in assets]):
                    logger.info(f"User {user_id} has nft of collection {chat_nft_collection}")
                    await bot.send_message(chat_id, get_message_text("join_request_accepted"))
                    return

    await bot.ban_chat_member(chat_id, user_id, until_date=30, revoke_messages=True, request_timeout=10)
    logger.info(f"User {user_id} banned from chat {chat_id}")
