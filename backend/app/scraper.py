import json
import asyncio
import logging
import random
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def run_scraper_with_cookies(search_query: str):
    logger.info(f"!!! SCRAPER STARTING: Query='{search_query}'")
    async with async_playwright() as p:
        try:
            # 1. Launch with Native Stealth
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
            )
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # 2. Strict Cookie Injection (Correcting Firefox values)
            try:
                with open('cookies.json', 'r') as f:
                    raw_cookies = json.load(f)
                
                formatted_cookies = []
                for c in raw_cookies:
                    cookie = {
                        "name": str(c["name"]),
                        "value": str(c["value"]),
                        "domain": ".ubereats.com",
                        "path": "/",
                        "secure": True
                    }
                    ss = c.get("sameSite", "Lax").lower()
                    if ss == "no_restriction": cookie["sameSite"] = "None"
                    elif ss == "unspecified": cookie["sameSite"] = "Lax"
                    else: cookie["sameSite"] = "Lax"
                    formatted_cookies.append(cookie)
                
                await context.add_cookies(formatted_cookies)
                logger.info(f"SCRAPER: {len(formatted_cookies)} cookies applied.")
            except Exception as e:
                logger.error(f"Cookie injection failed: {e}")

            # 3. Navigation
            url = f"https://www.ubereats.com/ca/search?q={search_query}"
            logger.info(f"SCRAPER: Navigating to {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=40000)

            # 4. FORCE HYDRATION (The "Scroll-Wake" Protocol)
            logger.info("SCRAPER: Forcing price hydration via scrolls...")
            # Scroll down and back up twice to force the lazy-loader to wake up
            for _ in range(2):
                await page.mouse.wheel(0, 1500)
                await asyncio.sleep(2)
                await page.mouse.wheel(0, -1000)
                await asyncio.sleep(1)

            # 5. Extraction Logic (The "Deep Text" Extractor)
            results = await page.evaluate(r"""() => {
                const links = Array.from(document.querySelectorAll('a[href*="/store/"]'));
                const seen = new Set();
                
                return links.map(link => {
                    const nameTag = link.querySelector('h3, h4, span[data-testid="rich-text"]');
                    const name = nameTag ? nameTag.innerText.trim() : "Unknown";
                    
                    // Uber 2026 Price Format Check
                    // We check textContent because it finds text that innerText sometimes misses
                    const fullText = link.textContent;
                    const priceMatch = fullText.match(/\$\d+\.\d+/);
                    
                    // Promo Check (Buy 1, BOGO, 1 free, Spend $X Get $Y)
                    const promoKeywords = ["Buy 1", "BOGO", "1 free", "free item", "Offer", "Spend"];
                    const hasPromo = promoKeywords.some(word => fullText.includes(word));
                    
                    return {
                        "restaurant_name": name,
                        "price_str": priceMatch ? priceMatch[0] : "N/A",
                        "promo": hasPromo ? "BOGO" : null
                    };
                }).filter(item => {
                    if (item.restaurant_name === "Unknown" || seen.has(item.restaurant_name)) return false;
                    seen.add(item.restaurant_name);
                    return true;
                });
            }""")

            await browser.close()
            logger.info(f"!!! SUCCESS: Found {len(results)} items at UVic.")
            return results

        except Exception as e:
            logger.error(f"!!! ERROR: {str(e)}")
            return [{"error": str(e)}]