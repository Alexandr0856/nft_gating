import aiohttp

from TonTools import LsClient, Wallet, NftItem

from blockchain.bc_tools import BlockchainTools


class TonTools(BlockchainTools):
    API_URL = "https://tonapi.nftscan.com/api"
    API_KEY = "XRU6Mp8YxdZEPMo9svkVhcec"

    def __init__(self):
        self.client = LsClient(ls_index=2, default_timeout=20)

    async def init_tonlib(self):
        await self.client.init_tonlib()

    async def create_wallet(self) -> tuple[str, str]:
        wallet = Wallet(provider=self.client)
        return wallet.address, wallet.mnemonics

    async def mint_nft(self, collection_address: str, recipient_address: str) -> str:
        # todo: implement
        return Exception("Not implemented")

    async def get_nft_owner(self, nft_address: str) -> str:
        item = NftItem(nft_address, provider=self.client)
        await item.update()

        return item.owner if item.sale is None else item.sale.owner

    async def get_nft_collection(self, nft_address: str) -> str:
        item = NftItem(nft_address, provider=self.client)
        await item.update()

        return item.collection_address

    async def get_assets_from_wallet(self, wallet: str):
        header = {"X-API-KEY": self.API_KEY}

        async with aiohttp.ClientSession(headers=header) as session:
            request = f"{self.API_URL}/ton/account/own/all/{wallet}"
            async with session.get(request) as response:
                res = await response.json()

                if res["status"] != 200:
                    return None

                if res["data"] is None:
                    return None

                return res["data"]
