import json
import asyncio
from playwright.async_api import async_playwright

async def run_scraper_with_cookies(search_query: str):
    async with async_playwright() as p:
        # Launch browser (Set headless=False to watch it during the demo!)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # 1. Load and Clean Cookies
        try:
            with open('cookies.json', 'r') as f:
                raw_cookies = json.load(f)
            
            cleaned_cookies = []
            for c in raw_cookies:
                # Playwright fix for 'sameSite' values
                s_site = c.get("sameSite", "Lax")
                if s_site == "unspecified": s_site = "Lax"
                if s_site == "no_restriction": s_site = "None"
                
                cleaned_cookies.append({
                    "name": c["name"],
                    "value": c["value"],
                    "domain": c["domain"],
                    "path": c["path"],
                    "secure": c.get("secure", True),
                    "httpOnly": c.get("httpOnly", False),
                    "sameSite": s_site
                })
            await context.add_cookies(cleaned_cookies)
        except FileNotFoundError:
            return [{"error": "cookies.json missing"}]

        page = await context.new_page()
        
        # 2. Go to Search URL
        # Note: Your address is already in your cookies!
        url = f"https://www.ubereats.com/ca/search?q={search_query}"
        await page.goto(url, wait_until="networkidle")

        # 3. The "Extraction" Magic
        # We wait for the first h3 (restaurant name) to appear
        await page.wait_for_selector('h3', timeout=10000)

        results = await page.evaluate("""() => {
            const cards = Array.from(document.querySelectorAll('a[href*="/store/"]'));
            return cards.map(card => {
                const name = card.querySelector('h3')?.innerText;
                const text = card.innerText;
                
                // Regex to find prices ($10.99) and ratings (4.5)
                const priceMatch = text.match(/\$\d+\.\d+/);
                const ratingMatch = text.match(/(\d\.\d)\s\(/);
                
                return {
                    "restaurant_name": name || "Unknown",
                    "price_str": priceMatch ? priceMatch[0] : "N/A",
                    "rating": ratingMatch ? ratingMatch[1] : "N/A",
                    "promo": text.includes("Buy 1") ? "BOGO" : null,
                    "is_ad": text.includes("Sponsored")
                };
            }).filter(item => item.restaurant_name !== "Unknown");
        }""")

        await browser.close()
        return results