#!/usr/bin/env python3
"""
Blocket Skrapare för OpenClaw-hårdvara - RIKTIG VERSION
Söker efter Mac mini och mini-PC på Blocket.se
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin, quote, unquote
import time
from bs4 import BeautifulSoup

class BlocketScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.blocket.se/'
        })
        self.results = []
        
    def search_blocket(self, query, category="15"):
        """
        Sök på Blocket
        category 15 = Datorer & Tillbehör (Stockholm som default)
        """
        try:
            # Blocket URL format
            encoded_query = quote(query)
            url = f"https://www.blocket.se/q/{encoded_query}/f?ca={category}&q={encoded_query}"
            
            print(f"🔍 Hämtar: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return self.parse_listings(response.text, query)
            
        except Exception as e:
            print(f"❌ Fel vid hämtning: {e}")
            return []
    
    def parse_listings(self, html, search_term):
        """Parsa HTML och extrahera annonser"""
        listings = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Blocket använder olika strukturer beroende på version
        # Försök hitta annonskort på olika sätt
        
        # Metod 1: Sök efter artikel-taggar med data-testid eller liknande
        articles = soup.find_all('article') or soup.find_all('div', class_=re.compile('.*[Aa]d.*'))
        
        # Metod 2: Sök efter länkar som innehåller /annons/
        ad_links = soup.find_all('a', href=re.compile(r'/annons/\d+'))
        
        print(f"   Hittade {len(articles)} artiklar och {len(ad_links)} annonslänkar")
        
        # Bearbeta annonslänkar
        seen_urls = set()
        for link in ad_links[:10]:  # Max 10 per sökning (var respektfull)
            try:
                href = link.get('href', '')
                if not href or href in seen_urls:
                    continue
                seen_urls.add(href)
                
                # Gör full URL om det behövs
                if href.startswith('/'):
                    href = f"https://www.blocket.se{href}"
                elif not href.startswith('http'):
                    continue
                
                # Hitta förälderelement för att få titel och pris
                parent = link.find_parent(['article', 'div', 'li'])
                
                title = link.get_text(strip=True) or "Okänd titel"
                
                # Försök hitta pris i närheten
                price = "N/A"
                if parent:
                    price_elem = parent.find(text=re.compile(r'\d+\s*kr')) or \
                                parent.find(string=re.compile(r'\d{3,6}'))
                    if price_elem:
                        if hasattr(price_elem, 'get_text'):
                            price = price_elem.get_text(strip=True)
                        else:
                            price = str(price_elem).strip()
                
                # Extrahera annons-ID från URL
                ad_id_match = re.search(r'/annons/(\d+)', href)
                ad_id = ad_id_match.group(1) if ad_id_match else "unknown"
                
                listings.append({
                    'title': title,
                    'price': price,
                    'url': href,
                    'ad_id': ad_id,
                    'search_term': search_term,
                    'description': f"Hittad via sökning: {search_term}"
                })
                
            except Exception as e:
                print(f"   ⚠️ Fel vid parsning av annons: {e}")
                continue
        
        return listings
    
    def scrape_all(self):
        """Huvudfunktion - sök alla relevanta termer"""
        print("=" * 60)
        print("🔍 BLOCKET SKRAPARE - RIKTIG VERSION")
        print("=" * 60)
        print("Söker efter Mac Mini och Mini-PC på Blocket...\n")
        print("⚠️  Varning: Respektfull scraping - max 10 resultat per sökning")
        print("-" * 60 + "\n")
        
        all_listings = []
        
        # Söktermer
        search_terms = [
            "mac mini",
            "apple mac mini",
            "intel nuc",
            "mini pc",
            "beelink"
        ]
        
        for term in search_terms:
            print(f"\n📱 Söker: '{term}'...")
            listings = self.search_blocket(term)
            
            if listings:
                print(f"   ✅ Hittade {len(listings)} annonser")
                all_listings.extend(listings)
            else:
                print(f"   ⚠️  Inga resultat eller fel")
            
            # Vänta mellan sökningar (var respektfull)
            time.sleep(2)
        
        # Ta bort duplikat baserat på URL
        unique_listings = {item['url']: item for item in all_listings}.values()
        
        print(f"\n{'=' * 60}")
        print(f"📊 Totalt: {len(unique_listings)} unika annonser hittade")
        print(f"{'=' * 60}\n")
        
        return list(unique_listings)
    
    def calculate_openclaw_score(self, item):
        """Beräkna OpenClaw-lämplighet (0-100)"""
        score = 0
        details = []
        
        title_lower = item.get('title', '').lower()
        
        # CPU-analys
        cpu_score = 0
        if 'm2' in title_lower:
            cpu_score = 30
            details.append("M2-chip: Utmärkt för AI")
        elif 'm1' in title_lower:
            cpu_score = 28
            details.append("M1-chip: Mycket bra för AI")
        elif 'i7' in title_lower or 'i9' in title_lower:
            cpu_score = 25
            details.append("Intel i7/i9: Bra prestanda")
        elif 'i5' in title_lower:
            cpu_score = 20
            details.append("Intel i5: Acceptabelt")
        elif 'ryzen' in title_lower:
            if 'ryzen 9' in title_lower or 'ryzen 7' in title_lower:
                cpu_score = 28
                details.append("Ryzen 7/9: Mycket bra")
            else:
                cpu_score = 22
                details.append("Ryzen 5: Bra")
        else:
            cpu_score = 15
            details.append("Okänd CPU")
        
        # RAM-analys (försök hitta i titel)
        ram_score = 0
        ram_match = re.search(r'(\d+)\s*gb', title_lower)
        if ram_match:
            ram_gb = int(ram_match.group(1))
            if ram_gb >= 32:
                ram_score = 25
                details.append(f"{ram_gb}GB RAM: Utmärkt")
            elif ram_gb >= 16:
                ram_score = 20
                details.append(f"{ram_gb}GB RAM: Mycket bra")
            elif ram_gb >= 8:
                ram_score = 12
                details.append(f"{ram_gb}GB RAM: Minimum")
            else:
                ram_score = 5
                details.append(f"{ram_gb}GB RAM: För lite")
        else:
            details.append("RAM ej specificerad i titel")
        
        # Prisanalys
        price_score = 0
        price_text = item.get('price', 'N/A')
        price_match = re.search(r'(\d{3,6})', price_text.replace(' ', '').replace('kr', ''))
        if price_match:
            price = int(price_match.group(1))
            if price <= 3000:
                price_score = 20
                details.append(f"{price}kr: Utmärkt pris")
            elif price <= 5000:
                price_score = 16
                details.append(f"{price}kr: Bra pris")
            elif price <= 8000:
                price_score = 12
                details.append(f"{price}kr: Acceptabelt pris")
            elif price <= 12000:
                price_score = 8
                details.append(f"{price}kr: Högt pris")
            else:
                price_score = 4
                details.append(f"{price}kr: Mycket högt pris")
        else:
            details.append("Pris ej specificerat")
        
        # Ström/effektivitet
        power_score = 0
        if 'm1' in title_lower or 'm2' in title_lower:
            power_score = 10
            details.append("Apple Silicon: Extremt strömsnål (6-20W)")
        elif 'nuc' in title_lower or 'beelink' in title_lower:
            power_score = 8
            details.append("Mini-PC: Strömsnål (15-65W)")
        else:
            power_score = 5
            details.append("Standard: Högre strömförbrukning")
        
        # Lagring (sätt alltid minimum om ej specificerat)
        storage_score = 5
        if 'ssd' in title_lower:
            storage_match = re.search(r'(\d+)\s*(gb|tb)', title_lower)
            if storage_match:
                size = int(storage_match.group(1))
                unit = storage_match.group(2)
                if unit == 'tb':
                    size *= 1000
                if size >= 1000:
                    storage_score = 15
                    details.append(f"{size//1000 if size>=1000 else size}TB SSD: Utmärkt")
                elif size >= 512:
                    storage_score = 12
                    details.append(f"{size}GB SSD: Mycket bra")
                elif size >= 256:
                    storage_score = 8
                    details.append(f"{size}GB SSD: Acceptabelt")
        
        total_score = cpu_score + ram_score + storage_score + price_score + power_score
        
        return {
            'score': total_score,
            'breakdown': {
                'cpu': cpu_score,
                'ram': ram_score,
                'storage': storage_score,
                'price': price_score,
                'power': power_score
            },
            'details': details,
            'recommendation': self.get_recommendation(total_score)
        }
    
    def get_recommendation(self, score):
        """Ge rekommendation baserat på score"""
        if score >= 80:
            return "🟢 KÖP NU - Utmärkt för OpenClaw 24/7"
        elif score >= 60:
            return "🟡 BRA DEAL - Värt att överväga"
        elif score >= 40:
            return "🟠 OK - Men kolla specs noggrant"
        else:
            return "🔴 AVVAKTA - Inte optimal för OpenClaw"
    
    def save_results(self, results, filename='blocket_openclaw_deals.json'):
        """Spara resultaten till JSON"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'search_criteria': 'Mac Mini, Mini-PC, NUC för OpenClaw',
            'total_results': len(results),
            'results': results
        }
        
        filepath = f"/Users/duljan/.openclaw/workspace/projects/openclaw-journey/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        print(f"💾 Resultat sparade till: {filename}")
        return filepath
    
    def print_report(self, results):
        """Skriv ut snygg rapport"""
        print("\n" + "=" * 60)
        print("📊 RANKING AV HITTADE ANNONSER")
        print("=" * 60)
        
        if not results:
            print("\n⚠️  Inga annonser hittades.")
            print("   Tips: Kolla manuellt på blocket.se")
            return
        
        for i, item in enumerate(results, 1):
            analysis = self.calculate_openclaw_score(item)
            
            print(f"\n{'─' * 60}")
            print(f"#{i} | {item['title']}")
            print(f"💰 Pris: {item.get('price', 'N/A')}")
            print(f"🔗 Länk: {item.get('url', 'N/A')}")
            print(f"🔍 Sökterm: {item.get('search_term', 'N/A')}")
            print(f"\n⭐ OPENCLAW-SCORE: {analysis['score']}/100")
            print(f"📋 {analysis['recommendation']}")
            print(f"\n📝 Analys:")
            for detail in analysis['details']:
                print(f"   ✓ {detail}")

if __name__ == '__main__':
    print("⚠️  STARTAR RIKTIG SKRAPNING MOT BLOCKET.SE")
    print("   Var respektfull - väntar mellan anrop\n")
    
    scraper = BlocketScraper()
    results = scraper.scrape_all()
    
    # Analysera och ranka
    analyzed_results = []
    for item in results:
        analysis = scraper.calculate_openclaw_score(item)
        item['analysis'] = analysis
        analyzed_results.append(item)
    
    # Sortera efter score
    analyzed_results.sort(key=lambda x: x['analysis']['score'], reverse=True)
    
    scraper.print_report(analyzed_results)
    scraper.save_results(analyzed_results)
    
    print("\n" + "=" * 60)
    print("✅ RIKTIG SKRAPNING KLAR!")
    print("=" * 60)
    print("\n📌 Nästa steg:")
    print("1. Klicka på länkarna ovan för att se annonserna")
    print("2. Kontakta säljare snabbt för bästa deals")
    print("3. Fråga om specifikationer om osäker")
    print("4. Vid köp - jag hjälper dig migrera allt!")
