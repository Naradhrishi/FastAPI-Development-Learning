from pwdlib import PasswordHash
from config import settings
import jwt
from datetime import datetime, timedelta, timezone


password_hash = PasswordHash.recommended()

# function to hash the plain password
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# function to verify hash password with plane password
def verify_password(password: str,  hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):
    # create the access token here to implement jwt in login system
    payload_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload_to_encode.update({"exp": expire})
    encoded_jwt_token = jwt.encode(payload_to_encode, settings.secret_key, algorithm=settings.jwt_encode_algo)
    return encoded_jwt_token

def create_refresh_token(data: dict):
    # create the access token here to implement jwt in login system
    payload_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    payload_to_encode.update({"exp": expire})
    encoded_jwt_token = jwt.encode(payload_to_encode, settings.secret_key, algorithm=settings.jwt_encode_algo)
    return encoded_jwt_token

def decode_jwt_token(encoded_jwt_token: str):
    return jwt.decode(encoded_jwt_token, settings.secret_key, algorithms=[settings.jwt_encode_algo])


