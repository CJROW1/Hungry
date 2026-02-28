import json
import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "deals.json")

class QuizPreferences(BaseModel):
    category: str
    vibe: str
    max_price: float
    min_rating: float
    dietary: str

def load_db():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

@app.post("/api/recommendations")
async def get_recommendations(prefs: QuizPreferences):
    db = load_db()
    matches = []
    
    # Define Weights (Total = 100)
    WEIGHTS = {
        "category": 40,
        "deal": 25,
        "rating": 20,
        "vibe": 15
    }

    for item in db:
        price_val = float(item["price"].replace("$", ""))
        item_rating = item.get("rating", 4.0)
        promo_text = item.get("promo", "").upper()
        
        # --- STRICT FILTERS ---
        if price_val > prefs.max_price or item_rating < prefs.min_rating:
            continue
        if prefs.dietary.lower() != "none":
            tags = (item["category"] + item.get("vibe", "")).lower()
            if prefs.dietary.lower() not in tags:
                continue

        # --- SCORING CALCULATION ---
        current_score = 0
        
        # 1. Category (40%)
        if prefs.category.lower() in item["category"].lower():
            current_score += WEIGHTS["category"]
            
        # 2. Deal Strength (25%)
        if "BOGO" in promo_text:
            current_score += WEIGHTS["deal"]
        elif "%" in promo_text or "OFF" in promo_text:
            current_score += (WEIGHTS["deal"] * 0.7)
        elif "FREE" in promo_text:
            current_score += (WEIGHTS["deal"] * 0.4)
            
        # 3. Rating Strength (20%)
        # Normalizes the rating (e.g., a 5.0 rating gets the full 20 points)
        rating_ratio = item_rating / 5.0
        current_score += (WEIGHTS["rating"] * rating_ratio)
        
        # 4. Vibe Match (15%)
        if prefs.vibe.lower() in item.get("vibe", "").lower():
            current_score += WEIGHTS["vibe"]

        # Final Match Percentage (capped at 100)
        match_percent = min(round(current_score), 100)
        
        matches.append({**item, "match_percentage": match_percent})

    # Sort by highest match percentage
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)

    return {
        "status": "success",
        "results": matches if matches else [i for i in db if "BOGO" in i.get("promo", "")]
    }