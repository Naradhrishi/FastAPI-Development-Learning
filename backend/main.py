# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow your React frontend to connect
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"], # React's default port
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Endpoint 1: A simple welcome message
# @app.get("/api/message")
# def get_message():
#     return {"text": "Hello from the FastAPI backend!"}

# # Endpoint 2: A simple data processing endpoint
# @app.get("/api/calculate")
# def get_calculation(number: int = 5):
#     return {"result": number * 2}

from fastapi import FastAPI, Body
from typing import Annotated, Optional


app = FastAPI()

#  STATIC PATH ROUTE or static endpoint
# fixed parameter based api should come first before dynamic one because it gets executed in top to down order
@app.get("/api/v1/message")
def get_message():
    return {"text": "Hello from the FastAPI backend!"}

# DYNAMIC PATH ENDPOINT / PATH PARAMETER ROUTE / 
@app.get("/api/v1/{message}")
def get_message(message: str):
    return {"your message": f'{message}'}


# QUERY PARAMETER ROUTE
# message query parameter based API endpoint where we can send query parameter
# we can make request using url http://127.0.0.1:8000/api/v1/?message=narad
# ==== NOTE : - cannot create separate endpoint blocks for the same HTTP method and URL path. In FastAPI
#  (and HTTP standards), a route is defined by the combination of its HTTP method (like GET) and its path (like /api/v1/)
# @app.get("/api/v1/")
# def get_message(message: str = ""):
#     return {"your message": f'{message}'}

# MULTIPLE QUERY PARAMETER ROUTE
@app.get("/api/v1/")
def get_message(name:str ="Guest", message: Optional[str]=None):
    if message:
        return {f"{name} message": f'{message}'}
    else:
        return {f'{name} message' : "no message has been send"}
        


@app.get("/api/v1/users")
def get_users():
    return {"all users" : ["ram","shyam"]}


@app.post("/api/v1/devs")
def create_dev(data_from_user: Annotated[dict[str , str | int], Body(title="create developer")]):
    print(data_from_user)
    return {"message": "user created", "data": data_from_user}

