import os
import aiohttp

from blockchain import BlockchainTools
from misc import Pg, logger

bot_token = os.getenv("BOT_TOKEN")
base_link = f"https://api.telegram.org/bot{bot_token}/"


async def generate_join_link(pg: Pg, bc_tools: BlockchainTools, user_id: int, nft_address: str) -> str | None:
    user_wallet = pg.get_wallet_address_by_user_id(user_id)
    nft_owner = await bc_tools.get_nft_owner(nft_address)

    if nft_owner != user_wallet:
        return Exception("User is not the owner of the item")

    grope_id = pg.get_group_by_collection(await bc_tools.get_nft_collection(nft_address))

    # user_info = requests.get(base_link + f"getChatMember?chat_id={grope_id}&user_id={user_id}").json()

    request = f"{base_link}createChatInviteLink?chat_id={grope_id}&member_limit=1&creates_join_request=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(request) as response:
            if response.status != 200:
                logger.error(f"Error while sending nft address to airdrop service: {response.status}")
                return

            join_link = await response.json()

            if join_link['ok'] and join_link['result'] and join_link['result']['invite_link']:
                return join_link['result']['invite_link']
