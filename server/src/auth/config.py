from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class AuthSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30
    refresh_token_cookie_key: str = "refresh_token"


auth_settings = AuthSettings()
