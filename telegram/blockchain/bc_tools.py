from abc import ABC, abstractmethod


class BlockchainTools(ABC):
    @abstractmethod
    async def create_wallet(self) -> tuple[str, str]:
        ...

    @abstractmethod
    async def mint_nft(self, collection_address: str, recipient_address: str) -> str:
        ...

    @abstractmethod
    async def get_nft_owner(self, nft_address: str) -> str:
        ...

    @abstractmethod
    async def get_nft_collection(self, nft_address: str) -> str:
        ...
