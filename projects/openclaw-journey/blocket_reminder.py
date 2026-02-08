#!/usr/bin/env python3
"""
Blocket Påminnelse - Skickar påminnelse att kolla Blocket manuellt
Eftersom automatisk skrapning blockeras
"""

import os
from datetime import datetime

def send_blocket_reminder():
    """Skicka påminnelse via Telegram"""
    
    message = """🔍 *Dags att kolla Blocket!*

Letar du fortfarande efter en Mini-PC/Mac Mini för OpenClaw?

🎯 *Bästa sökningarna just nu:*

*Mac Mini:*
• https://www.blocket.se/q/mac%20mini/f?cg=5000&q=mac%20mini
• https://www.blocket.se/q/mac%20mini%20m2/f?cg=5000&q=mac%20mini%20m2

*Mini-PC/NUC:*
• https://www.blocket.se/q/intel%20nuc/f?cg=5000&q=intel%20nuc
• https://www.blocket.se/q/beelink/f?cg=5000&q=beelink

💡 *Tips:*
- Sätt upp bevakningar på Blocket (kräver inloggning)
- Kolla 2-3 gånger per dag
- Skicka länk till mig för analys!

*Hittade du något? Skicka länken så räknar jag ut score!* ⭐"""
    
    # Skicka via OpenClaw message tool
    os.system(f'openclaw message send "5143277176" "{message}"')
    print(f"✅ Påminnelse skickad: {datetime.now()}")

if __name__ == '__main__':
    send_blocket_reminder()
