# ============= V3 =============
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from model import User, SignupUser, SignupResponse, LoginUser, LoginResponse
from typing import List
from pydantic import EmailStr
from auth import hash_password, verify_password, create_access_token, create_refresh_token
from config import settings



# with and yield are called as context manager in Python and latest version support async with yield which is async context manager
# event to handle db and table creation 
@asynccontextmanager
async def on_setup(app: FastAPI):
    #  write everything before yield what you wanna execute on startup
    create_db_and_tables()
    print("table created")

    yield
    #  now write the closing database code after yield
    print("everything closed")

app = FastAPI(lifespan = on_setup)

# # get API to fetch all users data
# @app.get("/api/v3/users", response_model = List[User], status_code = 200)
# async def get_all_users(session: Session = Depends(get_session)):
#     query = select(User)
#     users = session.exec(query).all()
#     return users

    
# # apis to handle database as well 
# @app.post("/api/v3/users", response_model=User, status_code=201)
# async def create_user(user: User, session: Session = Depends(get_session)):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.patch("/api/v3/users/{user_id}",  response_model = User)
# async def update_user(
#     user_id: int,
#     update_user: UpdateUser,
#     session: Session = Depends(get_session)
#     ):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code = 404, detail = "User not found!")
#     else:
#         update_user_sent_data = update_user.model_dump(exclude_unset = True)

#         for key, value in update_user_sent_data.items():
#             # setattr(object_name, attribute_name_string, new_value_to_set)
#             setattr(user, key, value)

#         session.add(user)
#         session.commit()
#         session.refresh(user)

#         return user


#         # THIS IS NOT safe and best practice so use model_dump instead to convert from Python object to Python dictionary
#         # if update_user.name is not None:
#         #     user.name = update_user.name
        
#         # if update_user.age is not None:
#         #     user.age = update_user.age
        
#         # if update_user.is_married is not None:
#         #     user.is_married = update_user.is_married
        
#         # session.commit()
#         # session.refresh(user)
#         # return user

# @app.delete("/api/v3/users/{user_id}")
# async def delete_user_with_id(user_id: int, session: Session = Depends(get_session)):
#     query = select(User).where(User.id == user_id)
#     user = session.exec(query).one()

#     session.delete(user)
#     session.commit()
#     print(f'user with id {user_id} got deleted!')



#============== V4 ============
@app.post("/api/v4/signup", response_model=SignupResponse, status_code = 201)
async def sign_up(data: SignupUser, session: Session = Depends(get_session)):
    # after getting the data first we have to store the data in database by checking that this email already exist or not?
    existing_user = session.exec(select(User).where(User.email == data.email)).first()
    if not existing_user:
        # if this email based user does not exist then insert data into users table otherwise raise HTTPError that this user already exist
        # before insertion make sure to hash the password before storing in database
        hashed_password = hash_password(data.password)
        about_to_insert_user = User(
            name = data.name,
            email = data.email,
            password = hashed_password
        )
        session.add(about_to_insert_user)
        session.commit()
        return {
            "message" : "Successfully signed up!",
            "name": data.name,
            "email": data.email
        }

    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'User already exist! Try another email.')


@app.post("/api/v4/login", response_model = LoginResponse)
async def login(user: LoginUser, session: Session = Depends(get_session)):
    # now first verify and check that is there any user exist with this credential or not?
    # if exist then return JWT Access and Refresh token and if not then return appropriate message
    signed_up = session.exec(select(User).where(User.email == user.email)).first()
    
    if not signed_up or not verify_password(user.password, signed_up.password):

        # redirect the user to the signup page or also show the message that user does not exist, kindly signup, first.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect email or password !")
    else:
        #  write the code here to generate access and refresh token
        payload = {"sub" : signed_up.email}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        return {
            "message" : "Successfully logged in !",
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "token_type" : "bearer"

        }



