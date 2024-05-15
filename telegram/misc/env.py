from os import environ


class TgKey:
    TOKEN: str = environ.get("BOT_TOKEN", "define me")


class PostgresEnv:
    USER: str = environ.get("POSTGRES_USER", "define me")
    HOST: str = environ.get("POSTGRES_HOST", "define me")
    PORT: int = int(environ.get("POSTGRES_PORT", "define me"))
    PASSWORD: str = environ.get("POSTGRES_PASSWORD", "define me")
    DB_NAME: str = environ.get("POSTGRES_DB", "define me")
