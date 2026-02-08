#!/usr/bin/env python3
"""
Blocket Browser Automation Skrapare
Använder Playwright för att styra en riktig webbläsare
Ser ut som en vanlig användare för att undvika blockering
"""

import json
import re
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

class BlocketBrowserScraper:
    def __init__(self, headless=False):
        """
        headless=False: Visar webbläsaren (bra för debugging)
        headless=True: Kör i bakgrunden (snabbare)
        """
        self.headless = headless
        self.results = []
        
    def search_blocket(self, search_term, category="5000"):
        """
        Sök på Blocket med riktig webbläsare
        category 5000 = Datorer
        """
        with sync_playwright() as p:
            # Starta webbläsare
            print(f"🚀 Startar webbläsare...")
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            try:
                # Bygg URL
                url = f"https://www.blocket.se/q/{search_term}/f?cg={category}&q={search_term}"
                print(f"🔍 Går till: {url}")
                
                # Gå till sidan
                page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Vänta på att annonser laddas (Blocket använder ofta JS)
                print(f"⏳ Väntar på att sidan laddas...")
                time.sleep(3)  # Ge JS tid att köra
                
                # Scrolla ner för att ladda mer (om infinite scroll)
                print(f"📜 Scrollar ner...")
                for i in range(3):
                    page.keyboard.press('End')
                    time.sleep(1)
                
                # Extrahera annonser
                print(f"📋 Hämtar annonser...")
                listings = self._extract_listings(page, search_term)
                
                print(f"✅ Hittade {len(listings)} annonser för '{search_term}'")
                
                browser.close()
                return listings
                
            except Exception as e:
                print(f"❌ Fel: {e}")
                browser.close()
                return []
    
    def _extract_listings(self, page, search_term):
        """Extrahera annonsdata från sidan"""
        listings = []
        
        # Försök hitta annons-element med olika selektorer
        # Blocket ändrar ofta sin HTML-struktur
        
        selectors = [
            'article a[href*="/annons/"]',  # Vanligast
            '[data-testid="ad-list-item"] a',
            '.ad-card a',
            'a[href*="/annons/"]'
        ]
        
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"   Använder selektor: {selector} ({len(elements)} element)")
                    break
            except:
                continue
        else:
            print("   ⚠️  Kunde inte hitta annonser med kända selektorer")
            # Spara HTML för debugging
            html = page.content()
            with open('/tmp/blocket_debug.html', 'w') as f:
                f.write(html)
            print("   💾 Sparade HTML till /tmp/blocket_debug.html")
            return []
        
        seen_urls = set()
        for element in elements[:15]:  # Max 15 per sökning
            try:
                # Hitta länk
                href = element.get_attribute('href')
                if not href or href in seen_urls:
                    continue
                seen_urls.add(href)
                
                # Gör full URL
                if href.startswith('/'):
                    href = f"https://www.blocket.se{href}"
                
                # Hitta titel (text i länken eller närliggande element)
                title = element.inner_text().strip() or "Okänd titel"
                
                # Försök hitta pris (i parent eller sibling)
                price = "N/A"
                parent = element.evaluate('el => el.closest("article, div, li")')
                if parent:
                    price_elem = page.query_selector('text=\\d+\\s*kr')
                    if price_elem:
                        price = price_elem.inner_text().strip()
                
                # Extrahera annons-ID
                ad_id_match = re.search(r'/annons/(\\d+)', href)
                ad_id = ad_id_match.group(1) if ad_id_match else "unknown"
                
                listings.append({
                    'title': title,
                    'price': price,
                    'url': href,
                    'ad_id': ad_id,
                    'search_term': search_term
                })
                
            except Exception as e:
                print(f"   ⚠️  Fel vid parsning: {e}")
                continue
        
        return listings
    
    def scrape_all(self):
        """Huvudfunktion - sök alla relevanta termer"""
        print("=" * 60)
        print("🔍 BLOCKET BROWSER AUTOMATION SKRAPARE")
        print("=" * 60)
        print("Använder riktig webbläsare för att se ut som vanlig användare")
        print("-" * 60 + "\\n")
        
        all_listings = []
        
        search_terms = [
            "mac mini",
            "intel nuc", 
            "mini pc",
            "beelink"
        ]
        
        for term in search_terms:
            print(f"\\n📱 Söker: '{term}'...")
            listings = self.search_blocket(term)
            
            if listings:
                all_listings.extend(listings)
                print(f"   ✅ {len(listings)} annonser")
            else:
                print(f"   ⚠️  Inga resultat")
            
            # Vänta mellan sökningar (var respektfull)
            time.sleep(2)
        
        # Ta bort duplikat
        unique = {item['url']: item for item in all_listings}.values()
        
        print(f"\\n{'=' * 60}")
        print(f"📊 Totalt: {len(unique)} unika annonser")
        print(f"{'=' * 60}\\n")
        
        return list(unique)

# Import från tidigare för scoring
import sys
sys.path.insert(0, '/Users/duljan/.openclaw/workspace/projects/openclaw-journey')
from blocket_scraper import BlocketScraper

class BlocketBrowserScraperWithScoring(BlocketBrowserScraper):
    """Kombinerar browser scraping med scoring algoritm"""
    
    def analyze_results(self, results):
        """Analysera resultat med scoring"""
        base_scraper = BlocketScraper()
        analyzed = []
        
        for item in results:
            analysis = base_scraper.calculate_openclaw_score(item)
            item['analysis'] = analysis
            analyzed.append(item)
        
        # Sortera efter score
        analyzed.sort(key=lambda x: x['analysis']['score'], reverse=True)
        return analyzed
    
    def save_and_report(self, results, filename='blocket_browser_results.json'):
        """Spara och skriva rapport"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'method': 'browser_automation',
            'total_results': len(results),
            'results': results
        }
        
        filepath = f"/Users/duljan/.openclaw/workspace/projects/openclaw-journey/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Sparade till: {filename}")
        
        # Skriv rapport
        print("\\n📊 RANKING:")
        for i, item in enumerate(results[:10], 1):
            analysis = item['analysis']
            print(f"\\n#{i} | {item['title'][:60]}...")
            print(f"   💰 {item.get('price', 'N/A')} | ⭐ {analysis['score']}/100")
            print(f"   📋 {analysis['recommendation']}")

if __name__ == '__main__':
    # Kör med synlig webbläsare första gången (så Adrian ser)
    print("🎬 Startar browser automation...")
    print("   Du kommer se en Chrome-fönster öppnas")
    print("   (Stäng det inte förrän skrapningen är klar!)\\n")
    
    scraper = BlocketBrowserScraperWithScoring(headless=False)
    results = scraper.scrape_all()
    
    if results:
        analyzed = scraper.analyze_results(results)
        scraper.save_and_report(analyzed)
        
        # Skicka notifiering om bra deals
        good_deals = [r for r in analyzed if r['analysis']['score'] >= 60]
        if good_deals:
            print(f"\\n🚨 Hittade {len(good_deals)} bra deals!")
            print("   Skickar notifiering...")
            # Här skulle vi skicka Telegram-notis
    else:
        print("\\n⚠️  Inga resultat. Kolla /tmp/blocket_debug.html")
    
    print("\\n✅ KLAR!")
