# Första Automationen - Blocket Skrapare

**Status:** ✅ KLAR
**Skapad:** 2026-02-09
**Syfte:** Hitta perfekt hårdvara för OpenClaw 24/7-drift

## Vad byggdes

En Python-skrapare som:
1. Analyserar Blocket-annonser efter Mac Mini/Mini-PC
2. Beräknar "OpenClaw-score" baserat på prestanda/pris/ström
3. Rankar deals från bäst till sämst
4. Sparar resultat i JSON för vidare analys

## Teknisk implementation

### Algoritm för scoring:
```
Total Score = CPU(30%) + RAM(25%) + Storage(15%) + Price(20%) + Power(10%)
```

### Viktiga funktioner:
- Regex-extraktion av specs från annonstexter
- Normalisering av pris/specs för jämförelse
- Kategorisering av rekommendationer (🟢🟡🟠🔴)
- JSON-export för automatisk bearbetning

## Resultat från första körning

| Rang | Produkt | Score | Pris | Rekommendation |
|------|---------|-------|------|----------------|
| 1 | Beelink Ryzen 7 32GB | 66/100 | 5200 kr | 🟡 Bra deal |
| 2 | Mac Mini M2 16GB | 65/100 | 7500 kr | 🟡 Bra deal |
| 3 | Mac Mini M1 8GB | 55/100 | 4500 kr | 🟠 OK |
| 4 | Intel NUC i5 | 53/100 | 2800 kr | 🟠 OK |

## Nästa förbättringar

- [ ] Automatisk notifiering via Telegram när score > 70 hittas
- [ ] Integration med Blocket API (om tillgängligt)
- [ ] Prishistorik för att se trender
- [ ] Automatisk kontakt av säljare (via mail/Telegram)

## Filstruktur

```
projects/openclaw-journey/
├── blocket_scraper.py          # Huvudskriptet
├── BLOCKET_SCRAPER_README.md   # Dokumentation
├── blocket_openclaw_deals.json # Senaste resultat
└── PROJECT.md                  # Övergripande projektplan
```

## Migration till ny hårdvara

När vi hittar och köper rätt dator:
1. Exportera all konfiguration från nuvarande Mac
2. Installera OpenClaw på nya maskinen
3. Migrera Klaus-inställningar (IDENTITY.md, SOUL.md, etc.)
4. Testa all funktionalitet
5. Uppdatera dokumentation

## Inlärningar

- Regex är kraftfullt för att parsa ostrukturerad text
- Viktigt att vara respektfull mot Blockets servrar (rate limiting)
- Att ranka baserat på multipla kriterier ger bättre resultat än enkel prisjämförelse

## Committed till GitHub

Se: https://github.com/klausaiadrian/openclaw-journey
