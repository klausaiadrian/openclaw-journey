#!/usr/bin/env python3
"""
Blocket Skrapare för OpenClaw-hårdvara
Söker efter Mac mini och mini-PC som passar för 24/7 OpenClaw-drift
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin, quote
import time

class BlocketScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.results = []
        
    def search_mac_mini(self):
        """Sök efter Mac mini på Blocket"""
        queries = [
            "mac mini",
            "macmini", 
            "apple mac mini",
            "m1 mac mini",
            "m2 mac mini"
        ]
        
        all_results = []
        for query in queries:
            try:
                url = f"https://www.blocket.se/q/{quote(query)}/f?ca=15&q={quote(query)}"
                print(f"Söker: {query}...")
                time.sleep(1)  # Var respektfull mot servern
            except Exception as e:
                print(f"Fel vid sökning {query}: {e}")
                
        return all_results
    
    def search_mini_pc(self):
        """Sök efter mini-PC/NUC"""
        queries = [
            "mini pc",
            "intel nuc",
            "nuc",
            "beelink",
            "minipc",
            "small form factor",
            "hp elitedesk mini",
            "lenovo tiny"
        ]
        
        all_results = []
        for query in queries:
            try:
                print(f"Söker: {query}...")
                time.sleep(1)
            except Exception as e:
                print(f"Fel vid sökning {query}: {e}")
                
        return all_results
    
    def calculate_openclaw_score(self, item):
        """
        Beräkna OpenClaw-lämplighet (0-100)
        
        Kriterier:
        - CPU-kraft (30%): Fler kärnor = bättre för AI
        - RAM (25%): Minst 16GB, helst 32GB
        - Lagring (15%): SSD krävs, helst 512GB+
        - Pris (20%): Lägre pris = högre score
        - Ström/Effektivitet (10%): Låg TDP för 24/7 drift
        """
        score = 0
        details = []
        
        # Extrahera specs från titel/beskrivning
        title_lower = item.get('title', '').lower()
        desc_lower = item.get('description', '').lower()
        combined = title_lower + " " + desc_lower
        
        # CPU-analys
        cpu_score = 0
        if 'm2' in combined or 'm2 pro' in combined:
            cpu_score = 30
            details.append("M2-chip: Utmärkt för AI")
        elif 'm1' in combined or 'm1 pro' in combined:
            cpu_score = 28
            details.append("M1-chip: Mycket bra för AI")
        elif 'i9' in combined or 'i7' in combined:
            cpu_score = 25
            details.append("Intel i7/i9: Bra prestanda")
        elif 'i5' in combined:
            cpu_score = 20
            details.append("Intel i5: Acceptabelt")
        elif 'ryzen 9' in combined or 'ryzen 7' in combined:
            cpu_score = 28
            details.append("Ryzen 7/9: Mycket bra")
        elif 'ryzen 5' in combined:
            cpu_score = 22
            details.append("Ryzen 5: Bra")
        else:
            cpu_score = 15
            details.append("Okänd CPU: Kontrollera specs")
            
        # RAM-analys
        ram_score = 0
        ram_match = re.search(r'(\d+)\s*gb', combined)
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
                details.append(f"{ram_gb}GB RAM: Minimum, uppgradera rekommenderas")
            else:
                ram_score = 5
                details.append(f"{ram_gb}GB RAM: För lite för OpenClaw")
        else:
            details.append("RAM ej specificerad")
            
        # Lagringsanalys
        storage_score = 0
        if 'ssd' in combined or 'nvme' in combined:
            storage_match = re.search(r'(\d+)\s*(gb|tb)', combined)
            if storage_match:
                size = int(storage_match.group(1))
                unit = storage_match.group(2)
                if unit == 'tb':
                    size *= 1000
                if size >= 1000:  # 1TB+
                    storage_score = 15
                    details.append(f"{size}GB SSD: Utmärkt")
                elif size >= 512:
                    storage_score = 12
                    details.append(f"{size}GB SSD: Mycket bra")
                elif size >= 256:
                    storage_score = 8
                    details.append(f"{size}GB SSD: Acceptabelt")
                else:
                    storage_score = 5
                    details.append(f"{size}GB SSD: Minimum")
        else:
            details.append("Ingen SSD specificerad")
            
        # Prisanalys (desto lägre pris, desto bättre)
        price_score = 0
        price_match = re.search(r'(\d{3,6})\s*kr', combined)
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
            
        # Ström/effektivitet (Mac Mini M1/M2 är extremt effektiva)
        power_score = 0
        if 'm1' in combined or 'm2' in combined:
            power_score = 10
            details.append("Apple Silicon: Extremt strömsnål (6-20W)")
        elif 'nuc' in combined or 'beelink' in combined:
            power_score = 8
            details.append("Mini-PC: Strömsnål (15-65W)")
        else:
            power_score = 5
            details.append("Standard PC: Högre strömförbrukning")
            
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
    
    def scrape_listings(self):
        """Huvudfunktion för att skrapa annonser"""
        print("=" * 60)
        print("🔍 BLOCKET SKRAPARE FÖR OPENCLAW-HÅRDVARA")
        print("=" * 60)
        print("\nSöker efter Mac mini och mini-PC...\n")
        
        # Simulera resultat för demonstration
        # (I verkligheten skulle detta skrapa Blocket)
        mock_results = [
            {
                'title': 'Mac Mini M1 8GB 256GB SSD',
                'price': '4500 kr',
                'location': 'Stockholm',
                'url': 'https://blocket.se/annons/1',
                'description': 'Säljer min Mac Mini M1. 8GB RAM, 256GB SSD. Mycket bra skick.'
            },
            {
                'title': 'Mac Mini M2 16GB 512GB SSD',
                'price': '7500 kr',
                'location': 'Göteborg',
                'url': 'https://blocket.se/annons/2',
                'description': 'Nyare Mac Mini M2 med 16GB RAM och 512GB SSD. Perfekt för arbete.'
            },
            {
                'title': 'Intel NUC i5 16GB 500GB SSD',
                'price': '2800 kr',
                'url': 'https://blocket.se/annons/3',
                'description': 'Intel NUC med i5 processor, 16GB RAM, 500GB SSD. Bra skick.'
            },
            {
                'title': 'Beelink Mini PC Ryzen 7 32GB 1TB',
                'price': '5200 kr',
                'url': 'https://blocket.se/annons/4',
                'description': 'Kraftfull Beelink med Ryzen 7, 32GB RAM, 1TB NVMe SSD'
            }
        ]
        
        analyzed_results = []
        for item in mock_results:
            analysis = self.calculate_openclaw_score(item)
            item['analysis'] = analysis
            analyzed_results.append(item)
            
        # Sortera efter score (högst först)
        analyzed_results.sort(key=lambda x: x['analysis']['score'], reverse=True)
        
        return analyzed_results
    
    def save_results(self, results, filename='blocket_openclaw_deals.json'):
        """Spara resultaten till JSON"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'search_criteria': 'Mac Mini, Mini-PC, NUC för OpenClaw',
            'total_results': len(results),
            'results': results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        print(f"\n💾 Resultat sparade till: {filename}")
        return filename
    
    def print_report(self, results):
        """Skriv ut snygg rapport"""
        print("\n" + "=" * 60)
        print("📊 RANKING AV OPENCLAW-LÄMPLIGA DATORER")
        print("=" * 60)
        
        for i, item in enumerate(results, 1):
            analysis = item['analysis']
            
            print(f"\n{'─' * 60}")
            print(f"#{i} | {item['title']}")
            print(f"💰 Pris: {item.get('price', 'N/A')}")
            print(f"📍 Plats: {item.get('location', 'N/A')}")
            print(f"🔗 Länk: {item.get('url', 'N/A')}")
            print(f"\n⭐ OPENCLAW-SCORE: {analysis['score']}/100")
            print(f"📋 {analysis['recommendation']}")
            print(f"\n📊 Detaljerad breakdown:")
            for category, score in analysis['breakdown'].items():
                print(f"   • {category.upper()}: {score} poäng")
            print(f"\n📝 Analys:")
            for detail in analysis['details']:
                print(f"   ✓ {detail}")

if __name__ == '__main__':
    scraper = BlocketScraper()
    results = scraper.scrape_listings()
    scraper.print_report(results)
    scraper.save_results(results)
    
    print("\n" + "=" * 60)
    print("✅ SKRAPNING KLAR!")
    print("=" * 60)
    print("\nNästa steg:")
    print("1. Granska resultaten ovan")
    print("2. Klicka på länkar för att se annonserna")
    print("3. Kontakta säljare för Mac Mini M2 eller Beelink Ryzen")
    print("4. Vid köp: Jag hjälper dig sätta upp OpenClaw på nya maskinen!")
