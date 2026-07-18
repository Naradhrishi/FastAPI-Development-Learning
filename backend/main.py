# ============= V3 =============
from fastapi import FastAPI, Depends, HTTPException, status, Request
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from model import User, UpdateUser
from typing import List
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter




# with and yield are called as context manager in Python and latest version support async with yield which is async context manager
# event to handle db and table creation 
@asynccontextmanager
async def on_setup(app: FastAPI):
    #  write everything before yield what you wanna execute on startup
    create_db_and_tables()
    print("table created")

    # connect to redis notebook here 
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)

    await FastAPILimiter.init(redis_connection)
    print("RATE LIMITER  ready and started", flush=True)

    yield
    #  now write the closing database code after yield

    # close redis notebook connection here
    await FastAPILimiter.close()
    print("REDIS CLOSED", flush=True)

    print("everything closed")

app = FastAPI(lifespan = on_setup)


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # do everything whatever needed to check or do before calling the actual api endpoint using call_next function
    print("Checked everything ok", flush=True)
    
    # as all ok so calling the API
    response = await call_next(request)

    # now check or do anything you want with response that we get from the API and if all ok then return the response
    print("Did whatever needed, now returning now...", flush=True)
    return response


# get API to fetch all users data
@app.get("/api/v3/users", response_model = List[User], status_code = 200)
async def get_all_users(session: Session = Depends(get_session)):
    query = select(User)
    users = session.exec(query).all()
    return users

    
# apis to handle database as well 
@app.post("/api/v3/users", response_model=User, status_code=201)
async def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.patch("/api/v3/users/{user_id}", dependencies = [Depends(RateLimiter(times = 2, seconds = 60))],  response_model = User)
async def update_user(
    user_id: int,
    update_user: UpdateUser,
    session: Session = Depends(get_session)
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    else:
        update_user_sent_data = update_user.model_dump(exclude_unset = True)

        for key, value in update_user_sent_data.items():
            # setattr(object_name, attribute_name_string, new_value_to_set)
            setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


        # THIS IS NOT safe and best practice so use model_dump instead to convert from Python object to Python dictionary
        # if update_user.name is not None:
        #     user.name = update_user.name
        
        # if update_user.age is not None:
        #     user.age = update_user.age
        
        # if update_user.is_married is not None:
        #     user.is_married = update_user.is_married
        
        # session.commit()
        # session.refresh(user)
        # return user

@app.delete("/api/v3/users/{user_id}")
async def delete_user_with_id(user_id: int, session: Session = Depends(get_session)):
    query = select(User).where(User.id == user_id)
    user = session.exec(query).one()

    session.delete(user)
    session.commit()
    print(f'user with id {user_id} got deleted!')



