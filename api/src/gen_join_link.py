import os
import requests

from TonTools import TonCenterClient, NftItem

from .pg_utils import get_connection, get_group_by_collection, get_user_wallet_by_id

bot_token = os.getenv("BOT_TOKEN")
base_link = f"https://api.telegram.org/bot{bot_token}/"


async def generate_join_link(user_id: int, nft_address: str) -> str:
    ton_client = TonCenterClient(base_url=os.getenv("TON_RPC"))

    db_conn = get_connection()
    db_cursor = db_conn.cursor()

    item = NftItem(nft_address, provider=ton_client)
    await item.update()

    user_wallet = get_user_wallet_by_id(db_cursor, user_id)
    nft_owner = item.owner if item.sale is None else item.sale.owner

    if nft_owner != user_wallet:
        return Exception("User is not the owner of the item")

    grope_id = get_group_by_collection(db_cursor, item.collection_address)

    user_info = requests.get(base_link + f"getChatMember?chat_id={grope_id}&user_id={user_id}").json()

    join_link = requests.get(base_link + f"createChatInviteLink?chat_id={grope_id}&member_limit=1").json()

    if join_link['ok'] and join_link['result'] and join_link['result']['invite_link']:
        return join_link['result']['invite_link']
