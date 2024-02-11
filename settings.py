from decouple import config


class Settings:
    API_HOST = config("API_HOST", default="127.0.0.1")
    API_PORT = int(config("API_PORT", default="8080"))
    SECRET = config("SECRET")
    ALGORITHM = config("ALGORITHM", default="HS")
    ADMIN_SECRET = config("ADMIN_SECRET")
    REFRESH_TOKEN_EXPIRY = 86400


settings = Settings()
