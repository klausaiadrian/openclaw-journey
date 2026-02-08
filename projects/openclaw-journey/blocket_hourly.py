#!/usr/bin/env python3
"""
Blocket Skrapare med Telegram-notifiering
Körs varje timme och skickar meddelande vid bra deals
"""

import subprocess
import json
import sys
sys.path.insert(0, '/Users/duljan/.openclaw/workspace/projects/openclaw-journey')
from blocket_scraper import BlocketScraper

def run_scraper_with_notifications():
    print("🔍 Startar Blocket-sökning...")
    
    scraper = BlocketScraper()
    results = scraper.scrape_listings()
    
    # Spara resultat
    scraper.save_results(results)
    
    # Hitta deals över 70 poäng
    good_deals = [r for r in results if r['analysis']['score'] >= 70]
    
    if good_deals:
        print(f"🎉 Hittade {len(good_deals)} bra deals!")
        
        # Skapa meddelande
        message = "🚨 *BRA DEALS HITTADE PÅ BLOCKET!*\n\n"
        
        for i, deal in enumerate(good_deals[:3], 1):  # Max 3 deals
            analysis = deal['analysis']
            message += f"*{i}. {deal['title']}*\n"
            message += f"💰 Pris: {deal.get('price', 'N/A')}\n"
            message += f"⭐ Score: {analysis['score']}/100\n"
            message += f"📋 {analysis['recommendation']}\n"
            message += f"🔗 {deal.get('url', 'N/A')}\n\n"
        
        message += "⚡ *Kontakta säljaren snabbt för bästa chans!*"
        
        # Skicka via Telegram (använder OpenClaw's message tool via system)
        import os
        os.system(f'openclaw message send "5143277176" "{message}"')
        
        return True
    else:
        print("📊 Inga deals över 70p denna timme.")
        return False

if __name__ == '__main__':
    run_scraper_with_notifications()
