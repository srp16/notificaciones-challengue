from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt

password_hash = PasswordHash.recommended()

def hash_password(password: str)-> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    payload= {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, "private_key", algorithm="HS256")