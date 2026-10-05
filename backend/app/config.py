import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "SanitaSafe Analytical Engine"
    API_PREFIX: str = "/api"
    EARTHDATA_USERNAME: str = os.getenv("EARTHDATA_USERNAME", "")
    EARTHDATA_PASSWORD: str = os.getenv("EARTHDATA_PASSWORD", "")
    EARTHDATA_TOKEN: str = os.getenv("EARTHDATA_TOKEN", "")
    CACHE_DIR: str = os.getenv("SANITASAFE_CACHE_DIR", "./cache")
    ENABLE_LIVE_FETCH: bool = os.getenv("ENABLE_LIVE_FETCH", "true").lower() in ("true", "1", "yes")

settings = Settings()
