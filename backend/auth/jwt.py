from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import time
from typing import Dict

import jwt
from decouple import config


def token_response(token: str):
    return {
        "access_token": token
    }

JWT_SECRET = config('secret')


def signJWT(user_id: str) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 2400
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"))


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}

class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                print("Failed here.")
                raise HTTPException(status_code=403, detail="Invalid authentication token")

            if not self.verify_jwt(credentials.credentials):
                print("Failed here two")
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return credentials.credentials
        else:
            print("Failed here three")
            raise HTTPException(status_code=403, detail="Invalid authorization token")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid