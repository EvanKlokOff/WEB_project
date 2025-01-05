from pathlib import Path
from datetime import timedelta
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent
class JWT_auth(BaseModel):
    jwt_private_path:Path = BASE_DIR/'authorization'/'cert'/'jwt_private.pem'
    jwt_open_path:Path = BASE_DIR/'authorization'/'cert'/'jwt_public.pem'
    algorithm:str = "RS256"

class JWT_parametres(BaseModel):
    jwt_access_token_expire_time:timedelta = timedelta(seconds=180)
    jwt_refresh_token_expire_time:timedelta = timedelta(days=7)
    jwt_token_default_expire_time:timedelta = timedelta(hours=3)
jwt_parametres = JWT_parametres()
auth_jwt = JWT_auth()

if __name__ == "__main__":
    print(BASE_DIR)