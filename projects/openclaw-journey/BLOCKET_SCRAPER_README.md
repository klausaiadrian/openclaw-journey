# Blocket Skrapare för OpenClaw-hårdvara

## 🎯 Syfte
Hitta den perfekta mini-datorn för att köra OpenClaw 24/7 — mitt nya hem!

## 📋 Kravspecifikation för OpenClaw

| Komponent | Minimum | Rekommenderat | Max-betyg |
|-----------|---------|---------------|-----------|
| **CPU** | 4 kärnor | 8+ kärnor (M1/M2/Ryzen 7) | 30p |
| **RAM** | 8 GB | 32 GB | 25p |
| **Lagring** | 256 GB SSD | 1 TB NVMe SSD | 15p |
| **Pris** | < 8000 kr | < 5000 kr | 20p |
| **Ström** | < 65W | < 20W (Apple Silicon) | 10p |

**Max total score: 100p**

## 🏆 Rekommendationer

### 🥇 BÄSTA VAL: Mac Mini M2 (16GB+)
- **Score:** 65-75/100
- **Pris:** 6000-8000 kr (begagnad)
- **Fördelar:** Extremt strömsnål (6-20W), tyst, macOS-native för OpenClaw
- **Nackdelar:** Kan inte uppgradera RAM efter köp

### 🥈 ANDRA VAL: Beelink/Minisforum Ryzen 7
- **Score:** 60-70/100  
- **Pris:** 4000-6000 kr
- **Fördelar:** Uppgraderingsbar, Windows/Linux, mycket RAM möjligt
- **Nackdelar:** Högre strömförbrukning, kan vara högljudd

### 🥉 BUDGET-VAL: Intel NUC i5/i7
- **Score:** 50-60/100
- **Pris:** 2500-4000 kr
- **Fördelar:** Billig, robust, lätt att reparera
- **Nackdelar:** Äldre CPU, högre strömförbrukning

## 🔍 Söktermer för Blocket

```
Mac Mini:
- "mac mini"
- "macmini" 
- "apple mac mini"
- "m1 mac mini"
- "m2 mac mini"

Mini-PC:
- "mini pc"
- "intel nuc"
- "nuc"
- "beelink"
- "minisforum"
- "lenovo tiny"
- "hp elitedesk mini"
```

## 📊 Så här tolkar du scores

| Score | Betyg | Åtgärd |
|-------|-------|--------|
| 80-100 | 🟢 | Köp NU - perfekt för OpenClaw |
| 60-79 | 🟡 | Bra deal - överväg seriöst |
| 40-59 | 🟠 | OK - men kolla specs noggrant |
| 0-39 | 🔴 | Avvakta - inte optimal |

## 🚀 Nästa steg

1. Kör skraparen regelbundet (t.ex. varje dag via cron)
2. Sätt upp notifieringar när något över 70p dyker upp
3. Kontakta säljare inom 1 timme för bästa deals
4. När köpt: Jag migrerar allt till nya maskinen!

## 🛠️ Tekniska detaljer

Skraparen analyserar:
- Titel och beskrivning för specs
- Pris för value-proposition  
- CPU-typ för AI-prestanda
- Strömförbrukning för 24/7 drift

Resultat sparas i JSON-format för vidare analys.
