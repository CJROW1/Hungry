import json
import os
from fastapi import FastAPI

app = FastAPI()

# Get the path relative to this main.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "deals.json")

# Load the data at startup
try:
    with open(DATA_PATH, "r") as f:
        DEALS_DB = json.load(f)
except FileNotFoundError:
    print(f"ERROR: Could not find data at {DATA_PATH}")
    DEALS_DB = []

@app.get("/api/search")
async def search(q: str):
    query = q.lower()
    results = [
        item for item in DEALS_DB 
        if query in item["name"].lower() 
        or query in item["category"].lower() 
    ]
    return {"status": "success", "results": results}
    logger.info(f"!!! GATEWAY: Received request for {q}")
    try:
        results = await run_scraper_with_cookies(q)
        return {"status": "success", "query": q, "results": results}
    except Exception as e:
        logger.error(f"!!! GATEWAY ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/greeting")
async def greeting():
    return {"message": "Hello from Hungry Buddy Backend"}
