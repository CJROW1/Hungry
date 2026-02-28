import json
import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 1. CORS Configuration for React/Vite (Port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Path Logic for Docker/Arch Linux
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "deals.json")

# 3. The 5-Parameter Data Model
class QuizPreferences(BaseModel):
    category: str       # e.g., "Sushi", "Pizza"
    vibe: str           # e.g., "Student Staple", "Late Night"
    max_price: float    # User's budget limit
    min_rating: float   # Minimum quality (e.g., 4.0)
    dietary: str        # e.g., "Vegan", "Halal", "None"

def load_db():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# --- CORE LOGIC ---

@app.get("/api/search")
async def general_search(q: str = ""):
    """Standard search tool for the main landing page"""
    db = load_db()
    if not q: return {"results": db}
    
    query = q.lower()
    results = [
        item for item in db 
        if query in item["name"].lower() or 
           query in item["category"].lower() or 
           query in item.get("vibe", "").lower()
    ]
    return {"results": results}

@app.post("/api/recommendations")
async def get_recommendations(prefs: QuizPreferences):
    """The 'Brain' of the Page 1 to Page 2 flow"""
    db = load_db()
    matches = []

    for item in db:
        # Data Normalization
        price_val = float(item["price"].replace("$", ""))
        item_rating = item.get("rating", 4.0)
        promo_text = item.get("promo", "").upper()
        
        # --- PARAMETER 1: DIETARY (Strict Filter) ---
        if prefs.dietary.lower() != "none":
            searchable_tags = (item["category"] + item.get("vibe", "")).lower()
            if prefs.dietary.lower() not in searchable_tags:
                continue # Discard if it doesn't meet dietary needs

        # --- PARAMETER 2 & 3: PRICE & RATING (Strict Filters) ---
        if price_val > prefs.max_price or item_rating < prefs.min_rating:
            continue # Discard if too expensive or low quality

        # --- SCORING ENGINE (Strength of Deal + Matching) ---
        score = 0
        
        # Deal Strength Logic
        if "BOGO" in promo_text:
            score += 12  # BOGO is the king of deals
        elif "%" in promo_text or "OFF" in promo_text:
            score += 8   # High percentage value
        elif "FREE" in promo_text:
            score += 5   # Free item/side
        elif promo_text:
            score += 2   # Standard value pick

        # Parameter 4: Category Match (Primary weight)
        if prefs.category.lower() in item["category"].lower():
            score += 15
        
        # Parameter 5: Vibe Match (Secondary weight)
        if prefs.vibe.lower() in item.get("vibe", "").lower():
            score += 8
            
        # Quality Bonus
        score += (item_rating * 1.5)

        # Store result with its calculated score
        matches.append({**item, "match_score": round(score, 2)})

    # Sort results so the 'Perfect Match' + 'Best Deal' is first
    matches.sort(key=lambda x: x["match_score"], reverse=True)

    # Fallback: If no strict matches found, return top 4 BOGO deals generally
    if not matches:
        return {
            "status": "fallback",
            "message": "No perfect matches, but these are the strongest deals right now!",
            "results": [i for i in db if "BOGO" in i.get("promo", "")][:4]
        }

    return {"status": "success", "results": matches}

if __name__ == "__main__":
    import uvicorn
    # Listening on 0.0.0.0 is required for Docker access
    uvicorn.run(app, host="0.0.0.0", port=8000)
