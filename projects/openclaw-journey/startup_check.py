#!/usr/bin/env python3
"""
Startup Check - Ser efter missade deals när datorn varit avstängd
Körs automatiskt vid uppstart
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

CHECK_FILE = "/Users/duljan/.openclaw/workspace/projects/openclaw-journey/last_check.txt"

def check_missed_deals():
    now = datetime.now()
    
    # Läs senaste kontroll
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, 'r') as f:
            last_check_str = f.read().strip()
            last_check = datetime.fromisoformat(last_check_str)
    else:
        last_check = now - timedelta(hours=24)  # Första körning, kolla senaste 24h
    
    hours_missed = (now - last_check).total_seconds() / 3600
    
    if hours_missed > 1:
        print(f"📴 Datorn har varit avstängd i {hours_missed:.1f} timmar")
        print("🔍 Kollar efter missade deals...")
        
        # Kör skraparen
        import sys
        sys.path.insert(0, '/Users/duljan/.openclaw/workspace/projects/openclaw-journey')
        from blocket_scraper import BlocketScraper
        
        scraper = BlocketScraper()
        results = scraper.scrape_listings()
        
        # Hitta deals över 70p
        good_deals = [r for r in results if r['analysis']['score'] >= 70]
        
        if good_deals:
            message = f"🚨 *DU HAR MISSAT DEALS!*\n\n"
            message += f"Datorn var avstängd i {hours_missed:.1f} timmar.\n"
            message += f"Hittade {len(good_deals)} bra deals:\n\n"
            
            for i, deal in enumerate(good_deals[:3], 1):
                analysis = deal['analysis']
                message += f"*{i}. {deal['title']}*\n"
                message += f"💰 {deal.get('price', 'N/A')} | ⭐ {analysis['score']}/100\n\n"
            
            # Skicka via Telegram
            os.system(f'openclaw message send "5143277176" "{message}"')
            print("✅ Notis skickad om missade deals!")
        else:
            print("📊 Inga deals över 70p missade.")
    else:
        print(f"✅ Senaste kontroll för {hours_missed:.1f} timmar sedan - ingen avstängning")
    
    # Uppdatera timestamp
    with open(CHECK_FILE, 'w') as f:
        f.write(now.isoformat())

if __name__ == '__main__':
    check_missed_deals()
