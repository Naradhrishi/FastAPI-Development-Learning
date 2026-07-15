# from fastapi import FastAPI, Body, HTTPException, status, Path
# from typing import Annotated, Optional
# from pydantic import BaseModel, Field


# app = FastAPI()

# #  STATIC PATH ROUTE or static endpoint
# # fixed parameter based api should come first before dynamic one Because path operations are evaluated in order
# @app.get("/api/v1/message")
# def get_static_message():
#     return {"text": "Hello from the FastAPI backend!"}

# # DYNAMIC PATH ENDPOINT / PATH PARAMETER ROUTE / 
# @app.get("/api/v1/{message}")
# def get_dynamic_message(message: str):
#     return {"your message": f'{message}'}


# # QUERY PARAMETER ROUTE
# # message query parameter based API endpoint where we can send query parameter
# # we can make request using url http://127.0.0.1:8000/api/v1/?message=narad
# # ==== NOTE : - cannot create separate endpoint blocks for the same HTTP method and URL path. In FastAPI
# #  (and HTTP standards), a route is defined by the combination of its HTTP method (like GET) and its path (like /api/v1/)
# # @app.get("/api/v1/")
# # def get_message(message: str = ""):
# #     return {"your message": f'{message}'}

# # MULTIPLE QUERY PARAMETER ROUTE
# @app.get("/api/v1/")
# def get_query_message(name:str ="Guest", message: Optional[str]=None):
#     if message:
#         return {f"{name} message": f'{message}'}
#     else:
#         return {f'{name} message' : "no message has been send"}
        
# @app.get("/api/v1/profiles/{id}")
# def get_id(id: int):
#     return{"your id is: " : id}


# @app.get("/api/v1/users")
# def get_users():
#     return {"all users" : ["ram","shyam"]}

# # multiple path and query parameters
# @app.get("/api/v1/orders/{order_id}/items/{item_id}")
# async def get_order_and_item(order_id: int, item_id: int, price: float | None = None):
#     if not price:
#         return {
#             "your order" : order_id,
#             "item" : item_id,
#             "price" : price
#         }
#     else:
#         return {
#             "your order" : order_id,
#             "item" : item_id
#         }



# @app.post("/api/v1/devs")
# def create_dev(data_from_user: Annotated[dict[str , str | int], Body(title="create developer")]):
#     print(data_from_user)
#     return {"message": "user created", "data": data_from_user}



# #  Employee based ***CRUD*** based employee app which is version 2
# # NOTE :- using Annotated is latest and best practice 
# # and inside Annotated if we use Field then we don't have to use Body, Query, Path etc.. they all are just subclass of Field class

# employees_data = []
# class Address(BaseModel):
#     city: Annotated[str, Field(min_length=2)]
#     pin_code: Annotated[int, Field(gt=100000, le=999999 )]
# class Employee(BaseModel):
#     id: Annotated[int, Field(gt=0, title="Employee id", description="Employee id can't be duplicate")]
#     name: Annotated[str, Field(title="Employee name")]
#     age: Annotated[int, Field(gt=0, le=120, title="Employee age")]
#     address: Annotated[Address, Field(title="address of the employee")]

# # need to create a partial model for employee data update because our original employee model having all fields necessary

# class EmployeeUpdate(BaseModel):
#     name: Annotated[Optional[str], Field(default=None)] = None
#     age: Annotated[Optional[int], Field(default = None, ge=0, le=120)]
#     address: Annotated[Optional[Address], Field(description="it would be null if not provided")] = None

# #read data
# @app.get("/api/v2/employees")
# async def get_employee():
#     return employees_data


# @app.get("/api/v2/employees/{id}")
# async def get_employee_with_id(id: Annotated[int, Path(title="The ID of the employee", gt=0)]):
#     for emp in employees_data:
#         if emp.id == id:
#             return emp
#     raise HTTPException(status_code = 404, detail="Employee not found for this id")


# # This endpoint create employee
# @app.post("/api/v2/employees", status_code = status.HTTP_201_CREATED)
# async def create_employee(emp: Employee):
#     # create the employee here means add to the list
#     employees_data.append(emp)
#     return {
#         "message" : "Employee has been created successfully.",
#         "data" : emp
#     }

# #  for making update - for partial update we use PATCH and for total replace/full update use PUT
# @app.patch("/api/v2/employees/{id}")
# async def update_employee(id: int, patch_data: EmployeeUpdate):
#     for emp in employees_data:
#         if emp.id == id:
#             # how to update here and what data should i allow to update data
#             return {"message" : "updated corresponding data"}



# # Delete API endpoint
# @app.delete("/api/v2/employees/{id}", status_code=status.HTTP_200_OK)
# async def delete_employee_with_id(id: Annotated[int, Path(title="The ID of the employee", gt=0)]):
#         for emp in employees_data:
#             if emp.id == id:
#                 employees_data.remove(emp)
#                 return {
#                     "message" : f'Employee {id} as been deleted successfully.'
#                 }
#         raise HTTPException(status_code = 404, detail = "Employee not found with this id.")
        
        

# ============= V3 =============
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from model import User, UpdateUser
from typing import List



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

# @app.patch("/api/v3/{user_id}",  response_model = User)
# async def update_user(
#     user_id: int,
#     update_user: UpdateUser,
#     session: Session = Depends(get_session)
#     ):
#     existing_user = session.get(User, user_id)
#     if not existing_user:
#         raise HTTPException(status_code = 404, detail = "User not found!")
#     else:


# @app.delete("/api/v3/{user_id}")
# async def delete_user_with_id(user_id: int):


