from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default = None, primary_key=True)
    name: str = Field(nullable = False)
    age: int = Field(nullable = False)
    is_married: bool = Field(default = False)

class UpdateUser(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    is_married: Optional[bool] = None
    
