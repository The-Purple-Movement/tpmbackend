import os
from dotenv import load_dotenv

env = os.getenv("ENV", "dev")

if env == "prod":
    load_dotenv(".env.prod")
else:
    load_dotenv(".env.dev")

DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = env