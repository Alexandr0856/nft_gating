from aiogram import Bot
from aiogram.types import Message, Contact

from misc import Pg, Blockchains, GeneralStatus
from misc import logger, generate_join_link
from locales import get_message_text
from keyboards import get_contact_keyboard, remove_keyboard, invite_link_keyboard
from blockchain.ton_tools import TonTools


async def help_handler(message: Message, bot: Bot) -> None:
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(get_message_text("help", "us"))


async def start_handler(message: Message, bot: Bot, pg: Pg) -> None:
    logger.info(f"User {message.from_user.id} started the bot")

    bc_tools = TonTools()
    await bc_tools.init_tonlib()

    if not pg.is_user_exists(message.from_user.id):
        address, mnemonics = await bc_tools.create_wallet()

        wallet_id = pg.add_wallet(
            network=Blockchains.ton,
            address=address,
            secret=mnemonics
        )
        pg.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            wallet_id=wallet_id
        )

    if pg.is_user_has_phone(message.from_user.id):
        await message.answer(
            get_message_text("start", "us")
        )
    else:
        await message.answer(
            get_message_text("start", "us"),
            reply_markup=get_contact_keyboard()
        )

    if len(split_command := message.text.split()) > 1:
        airdrop_data = pg.get_airdrop_data(command=split_command[1])
        if airdrop_data:
            if airdrop_data["status"] != GeneralStatus.active:
                user_wallet = pg.get_wallet_address_by_user_id(message.from_user.id)
                nft_address = await bc_tools.mint_nft(airdrop_data["collection_address"], user_wallet)

                join_link = await generate_join_link(pg, bc_tools, message.from_user.id, nft_address)

                message_text = airdrop_data["message"].format(
                    username=message.from_user.username,
                )
                await message.answer(
                    message_text,
                    reply_markup=invite_link_keyboard(join_link)
                )
                return

            await message.answer(
                get_message_text("airdrop_is_not_active", "us")
            )
            return

        await message.answer(
            get_message_text("airdrop_not_found", "us")
        )
        return


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
