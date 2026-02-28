from fastapi import FastAPI
from .scraper import run_scraper_with_cookies
import logging

# Configure logging to show up in Docker
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")

app = FastAPI()

@app.get("/api/search")
async def search(q: str):
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
