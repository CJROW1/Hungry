import json
import asyncio
import logging
import random
# Import the module directly to avoid name collisions
import playwright_stealth
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def run_scraper_with_cookies(search_query: str):
    logger.info(f"!!! SCRAPER STARTING: Query='{search_query}'")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )

            page = await context.new_page()
            
            # THE FIX: Call the function directly from the module
            # This avoids the "module object is not callable" error
            await playwright_stealth.stealth(page)
            logger.info("SCRAPER: Stealth applied successfully.")

            # 1. Cookie Injection
            try:
                with open('cookies.json', 'r') as f:
                    raw_cookies = json.load(f)
                
                cleaned_cookies = []
                for c in raw_cookies:
                    domain = c.get("domain", "")
                    if "ubereats.com" in domain or "uber.com" in domain:
                        cleaned_cookies.append({
                            "name": c["name"],
                            "value": c["value"],
                            "domain": domain if domain.startswith('.') else f".{domain}",
                            "path": c.get("path", "/"),
                            "secure": True,
                            "sameSite": "Lax"
                        })
                await context.add_cookies(cleaned_cookies)
                logger.info("SCRAPER: Cookies injected.")
            except Exception as e:
                logger.error(f"Cookie Error: {e}")

            # 2. Navigation & Hydration
            url = f"https://www.ubereats.com/ca/search?q={search_query}"
            # Using 'commit' to get in fast, then we handle the wait manually
            await page.goto(url, wait_until="commit", timeout=30000)
            
            # Wait for the "Skeleton" to disappear and text to appear
            logger.info("SCRAPER: Waiting for content...")
            await asyncio.sleep(5) 
            await page.mouse.wheel(0, 1500)
            await asyncio.sleep(2)

            # 3. Extraction with 2026 Selectors
            results = await page.evaluate(r"""() => {
                const links = Array.from(document.querySelectorAll('a[href*="/store/"]'));
                const seen = new Set();
                
                return links.map(link => {
                    const nameTag = link.querySelector('h3, h4, span[data-testid="rich-text"]');
                    const name = nameTag ? nameTag.innerText.trim() : "Unknown";
                    const text = link.innerText;
                    
                    const price = text.match(/\$\d+\.\d+/);
                    const promo = ["Buy 1", "1 free", "BOGO", "Offer"].some(w => text.includes(w));
                    
                    return {
                        "restaurant_name": name,
                        "price_str": price ? price[0] : "N/A",
                        "promo": promo ? "BOGO" : null
                    };
                }).filter(item => {
                    if (item.restaurant_name === "Unknown" || seen.has(item.restaurant_name)) return false;
                    seen.add(item.restaurant_name);
                    return true;
                });
            }""")

            await browser.close()
            logger.info(f"!!! SUCCESS: Found {len(results)} items.")
            return results

        except Exception as e:
            logger.error(f"!!! GLOBAL ERROR: {str(e)}")
            return [{"error": str(e)}]