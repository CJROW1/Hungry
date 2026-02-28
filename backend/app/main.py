import json
import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
    
    # DEBUG: Print this to your terminal to ensure the Q&A answers are arriving
    print(f"Received Prefs: {prefs}") 

    for item in db:
        # Normalize data for comparison
        price_val = float(item["price"].replace("$", ""))
        item_rating = item.get("rating", 4.0)
        item_cat = item["category"].lower()
        
        # --- IMPROVED DYNAMIC FILTERING ---
        # If the user picks a category, we MUST prioritize it
        category_match = prefs.category.lower() in item_cat
        
        # If you have strict filters that are TOO tight, you'll always get 0 results
        # and hit your fallback. Let's make them slightly more flexible:
        if price_val > (prefs.max_price + 5): # $5 buffer
            continue
            
        current_score = 0
        
        # 1. Primary Category Match (Heavy Weight: 50pts)
        if category_match:
            current_score += 50
        elif any(word in item_cat for word in prefs.category.lower().split()):
            current_score += 25 # Partial credit for similar food
            
        # 2. Vibe Match (20pts)
        if prefs.vibe.lower() in item.get("vibe", "").lower():
            current_score += 20
            
        # 3. Deal & Rating (30pts)
        if "BOGO" in item.get("promo", "").upper():
            current_score += 15
        current_score += (item_rating * 3) # Max 15pts for a 5.0

        # Add a random tie-breaker so the order isn't static
        current_score += random.uniform(0, 1)

        matches.append({
            **item, 
            "match_percentage": min(round(current_score + 20), 100) # Base boost for high %
        })

    # Sort by the new dynamic score
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)

    # SUCCESS: Return the top matches for these specific answers
    if matches:
        return {"status": "success", "results": matches[:15]}
    
    # FALLBACK: If NO matches found, return a randomized selection of the DB
    # so it at least looks different than the previous "BOGO" list
    random_sample = random.sample(db, min(len(db), 10))
    return {"status": "success", "results": random_sample}