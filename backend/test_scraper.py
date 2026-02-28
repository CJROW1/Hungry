import asyncio
from app.scraper import get_uber_deals

async def main():
    print("Scouting deals near UVic...")
    deals = await get_uber_deals("Pizza")
    for deal in deals[:5]:
        print(f"Found: {deal['restaurant_name']} | BOGO: {deal['is_bogo']}")

if __name__ == "__main__":
    import asyncio
    results = asyncio.run(get_uber_deals("Sushi"))
    print(results)