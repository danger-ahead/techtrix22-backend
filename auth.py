from fastapi import HTTPException
import env_config
from cryptography.fernet import Fernet



"""
TODO: error in token of parameter. expecting bytes. use any method of encryption
"""


def check_token(token):
    token = token.encode("utf-8")
    fernet = Fernet(env_config.token_key)
    try:
        decToken = fernet.decrypt(token).decode()
        if decToken == env_config.username:
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=401, detail="validation failed")
