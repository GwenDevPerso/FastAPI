from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

    def get_uuid(self) -> Optional[UUID]:
        if self.user_id:
            return UUID(self.user_id)
        return None