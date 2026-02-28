from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import TypedDict
from pydantic import BaseModel

app = FastAPI()

# Allow your frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For the hackathon, "*" is fine. For production, specify your URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is reachable!"}

class GreetingRequest(BaseModel):
    name: str
    age: int

    
class GreetingResponse(BaseModel):
    message: str

@app.post("/greeting")
def greeting(request:GreetingRequest) -> GreetingResponse:
    return GreetingResponse(
        message = f"Hello {request.name} You are {request.age}"
    )
    