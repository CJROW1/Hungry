from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import TypedDict
from pydantic import BaseModel
from apify_client import ApifyClient
import os
from .scraper import run_scraper_with_cookies

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

@app.get("/api/search")
async def search_deals(q: str):
    # This calls the script you just pasted
    results = await run_scraper_with_cookies(q)
    return {"results": results}
    
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
    