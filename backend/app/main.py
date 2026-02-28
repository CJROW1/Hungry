import json
import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 1. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Path Logic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "deals.json")

# 3. The 5-Parameter Quiz Model
class QuizPreferences(BaseModel):
    category: str       # e.g., "Sushi", "Pizza"
    vibe: str           # e.g., "Student Staple", "Late Night"
    max_price: float    # User's budget
    min_rating: float   # e.g., 4.0
    dietary: str        # e.g., "Vegan", "Halal", "None"

def load_db():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# --- ROUTES ---

@app.get("/api/search")
async def general_search(q: str = ""):
    """Better Search: Partial matching across multiple fields"""
    db = load_db()
    if not q: return {"results": db}
    
    query = q.lower()
    results = []
    for item in db:
        # Check if query is in name, category, or vibe description
        if (query in item["name"].lower() or 
            query in item["category"].lower() or 
            query in item.get("vibe", "").lower()):
            results.append(item)
            
    return {"results": results}

@app.post("/api/recommendations")
async def get_recommendations(prefs: QuizPreferences):
    """5-Parameter Logic for Page 2"""
    db = load_db()
    matches = []

    for item in db:
        # Data Prep: Handle price formatting
        price_val = float(item["price"].replace("$", ""))
        item_rating = item.get("rating", 4.0) # Default if missing
        
        # --- SCORING & FILTERING ENGINE ---
        score = 0
        
        # A. Category Match (High Weight)
        if prefs.category.lower() in item["category"].lower():
            score += 15
        
        # B. Vibe Match (Medium Weight)
        if prefs.vibe.lower() in item.get("vibe", "").lower():
            score += 8

        # C. Dietary Filter (Strict)
        # Checks if the dietary requirement is mentioned in vibes or category
        if prefs.dietary.lower() != "none":
            searchable_tags = (item["category"] + item.get("vibe", "")).lower()
            if prefs.dietary.lower() not in searchable_tags:
                continue # Hard skip if it doesn't meet dietary needs

        # D. Price & Rating (Hard Filters)
        if price_val <= prefs.max_price and item_rating >= prefs.min_rating:
            # Bonus: Reward higher ratings in the score
            score += (item_rating * 2)
            matches.append({**item, "match_score": round(score, 2)})

    # Sort by Score (Descending)
    matches.sort(key=lambda x: x["match_score"], reverse=True)

    # Fallback Logic
    if not matches:
        return {
            "status": "fallback",
            "message": "Nothing perfectly matched, but here are the best BOGO deals!",
            "results": [i for i in db if i["promo"] == "BOGO"][:4]
        }

    return {"status": "success", "results": matches}
