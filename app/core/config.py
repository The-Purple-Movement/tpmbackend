import os
from dotenv import load_dotenv

env = os.getenv("ENV", "dev")

if env == "prod":
    load_dotenv(".env.prod")
else:
    load_dotenv(".env.dev")

DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = env

# JWT / Auth
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))