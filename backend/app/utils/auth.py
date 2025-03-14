import jwt
from datetime import datetime, timezone, timedelta
from typing import Literal, List
from utils.jwt_config import *

__all__ = ['create_token', 'get_token_payload', 'check_role']


def create_token(token_type: Literal['access', 'refresh'], payload: dict) -> str:
    if token_type not in ['access', 'refresh']:
        raise ValueError("token_type must be either 'access' or 'refresh'")
    
    if token_type == 'access':
        ttl = ACCESS_TOKEN_EXPIRATION_TIME
    if token_type == 'refresh':
        ttl = REFRESH_TOKEN_EXPIRATION_TIME

    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ttl)
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print("Created token:", token)

    return token


def get_token_payload(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return {'message': "Token has expired"}
    except jwt.InvalidTokenError:
        return {'message': "Invalid token"}
    

async def check_role(
    user_role: Literal['admin', 'manager', 'regular'], 
    allowed_roles: List[Literal['admin', 'manager', 'regular']]) -> bool:

    valid_roles = {'admin', 'manager', 'regular'}
    if user_role not in valid_roles:
        raise ValueError(f"Invalid user role: {user_role}. Must be one of {valid_roles}.")
    
    for role in allowed_roles:
        if role not in valid_roles:
            raise ValueError(f"Invalid allowed role: {role}. Must be one of {valid_roles}.")
        
    return user_role in allowed_roles