import env_config
from cryptography.fernet import Fernet



"""
TODO: error in token of parameter. expecting bytes. use any method of encryption
"""


def check_token(token):
    fernet = Fernet(env_config.token_key)
    decToken = fernet.decrypt(token).decode()
    print(fernet)
    if decToken == env_config.sername:
        return True
    return False
   


# b'GYGTv6fYyHPVXhPeMnOGLoEYDge8VFhAbMZ3GPRwH7E='
