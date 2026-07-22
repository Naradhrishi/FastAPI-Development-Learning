from fastapi import APIRouter, Depends, HTTPException
from database import get_session
from typing import Annotated, List
from sqlmodel import Session, select
from model import User

# if any such dependency or response or prefix , tags etc. required for all these APIs then we can include those directly in APIRouter object here
router = APIRouter(
    prefix="/users", 
    tags=["Users"],
    responses={404: {"description": "Item NOT found!"}}
    )

@router.get("/", response_model=List[User])
async def get_all_users(session: Annotated[Session, Depends(get_session)]):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=User)
async def get_user_with_id(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code = 404, detail="Item not found here")
    
    return user
