from uuid import UUID

from pydantic import BaseModel


class TokenAccess(BaseModel):
    access_token: str


class Token(TokenAccess):
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    exp: float
