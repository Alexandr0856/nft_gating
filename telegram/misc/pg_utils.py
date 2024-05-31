from dataclasses import dataclass
from psycopg2.extensions import connection


@dataclass
class Blockchains:
    solana = "SOL"
    ethereum = "ETH"
    binanceSmartChain = "BSC"
    base = "BASE"
    ton = "TON"


@dataclass
class GeneralStatus:
    active = "ACTIVE"
    inactive = "INACTIVE"
    deleted = "DELETED"


@dataclass
class WalletType:
    internal = "INTERNAL"
    external = "EXTERNAL"


class Pg:
    def __init__(self, conn: connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def is_user_exists(self, user_id: int) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return bool(self.cursor.fetchone())

    def is_user_has_phone(self, user_id: int) -> bool:
        self.cursor.execute("SELECT phone_number FROM users WHERE id = %s", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def is_user_has_email(self, user_id: int) -> bool:
        self.cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def is_user_has_birthday(self, user_id: int) -> bool:
        self.cursor.execute("SELECT birthday FROM users WHERE id = %s", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def is_user_has_ip_address(self, user_id: int) -> bool:
        self.cursor.execute("SELECT ip_address FROM users WHERE id = %s", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def add_wallet(
            self,
            network: Blockchains,
            address: str,
            secret: str,
            w_type: WalletType = WalletType.internal,
            status: GeneralStatus = GeneralStatus.active
    ) -> int:
        query = """
        INSERT INTO wallets (network, address, secret, type, status) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        data = (network, address, secret, w_type, status)
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def add_user(
            self,
            user_id: int,
            username: str,
            wallet_id: int,
            phone_number: str = None,
            email: str = None,
            birth_date: str = None,
            ip_address: str = None
    ) -> int:
        query = """
        INSERT INTO users (id, username, wallet_id, phone_number, email, birthday, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
        """

        data = (user_id, username, wallet_id, phone_number, email, birth_date, ip_address)
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def add_group(self, chat_id: int,  network: Blockchains, collection_address: str) -> int:
        query = """
        INSERT INTO protected_gropes (grope_id, network, collection_address) 
        VALUES (%s, %s, %s)
        RETURNING id
        """
        data = (chat_id, network, collection_address)
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def update_wallet_status(self, wallet_id: int, status: GeneralStatus) -> None:
        query = "UPDATE wallets SET status = %s WHERE id = %s"
        data = (status, wallet_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_user_phone(self, user_id: int, phone_number: str) -> None:
        query = "UPDATE users SET phone_number = %s WHERE id = %s"
        data = (phone_number, user_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_user_email(self, user_id: int, email: str) -> None:
        query = "UPDATE users SET email = %s WHERE id = %s"
        data = (email, user_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_user_birthday(self, user_id: int, birthday: str) -> None:
        query = "UPDATE users SET birthday = %s WHERE id = %s"
        data = (birthday, user_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_user_ip_address(self, user_id: int, ip_address: str) -> None:
        query = "UPDATE users SET ip_address = %s WHERE id = %s"
        data = (ip_address, user_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_group_status(self, chat_id: int, status: GeneralStatus) -> None:
        query = "UPDATE protected_gropes SET status = %s WHERE grope_id = %s"
        data = (status, chat_id)
        self.cursor.execute(query, data)
        self.conn.commit()

    def get_wallet_address_by_user_id(self, user_id: int) -> str:
        self.cursor.execute(
            "SELECT address FROM wallets JOIN users ON wallets.id = users.wallet_id WHERE users.id = %s",
            (user_id,)
        )
        return self.cursor.fetchone()[0]

    def get_airdrop_data(self, command: str, status: GeneralStatus = None) -> dict:
        if status:
            self.cursor.execute(
                "SELECT * FROM airdrop_commands WHERE command = %s AND status = %s",
                (command, status)
            )
        else:
            self.cursor.execute(
                "SELECT * FROM airdrop_commands WHERE command = %s",
                (command,)
            )

        return dict(self.cursor.fetchone())

    def get_nft_collection_by_group(self, chat_id: int) -> str:
        self.cursor.execute(
            "SELECT collection_address FROM protected_gropes WHERE grope_id = %s",
            (chat_id,)
        )
        return self.cursor.fetchone()[0]

    def get_group_by_collection(self, collection_address: str) -> int:
        self.cursor.execute(
            "SELECT grope_id FROM protected_gropes WHERE collection_address = %s",
            (collection_address,)
        )
        return self.cursor.fetchone()[0]
