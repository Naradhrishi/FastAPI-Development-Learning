from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default = None, primary_key=True)
    name: str = Field(nullable = False)
    email: EmailStr = Field(nullable = False, unique=True, index=True)
    password: str = Field(nullable = False)


class SignupUser(SQLModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)


class SignupResponse(SQLModel):
    message: str
    name: str
    email: EmailStr 
