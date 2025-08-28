# RTL-SDR Bandscope Monitor

Ez a projekt az **RTL-SDR** USB stick segítségével figyeli a 40m amatőrsáv (7.000–7.200 MHz) egy részét, és
**SQLite adatbázisba** menti a zajszinteket és jeleket.

## Funkciók
- RTL-SDR mintavételezés Pythonból (`pyrtlsdr`)
- Mért értékek mentése SQLite adatbázisba
- Későbbi feldolgozás és elemzés külön scriptben

## Rendszerkövetelmények
- Linux (Ubuntu/Debian/Devuan ajánlott)
- RTL-SDR stick
- Python 3.8+

## Telepítés

### 1. Rendszer előkészítése
```bash
sudo apt update
sudo apt install rtl-sdr python3 python3-pip python3-venv sqlite3
```

### 2. Virtuális környezet létrehozása
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Python csomagok telepítése
```bash
pip install -r requirements.txt
```

### 4. SQLite adatbázis előkészítése
Az első futtatáskor a script automatikusan létrehozza a `bandscope.db` adatbázist a `measurements` táblával:
```sql
CREATE TABLE IF NOT EXISTS measurements (
    timestamp INTEGER,
    freq INTEGER,
    power REAL
);
```

## Használat

Indítsd el a `collector.py` scriptet:
```bash
python collector.py
```

Ez folyamatosan mérni fog egy fix frekvenciát (pl. 7.040 MHz) és menti az eredményt az adatbázisba.

Az adatbázist bármikor meg tudod nézni:
```bash
sqlite3 bandscope.db
sqlite> SELECT * FROM measurements LIMIT 10;
```

## Tervek
- Sávszkennelés (7.000–7.050 MHz kezdetben, 2.5 kHz lépésekkel)
- Véletlenszerű hosszabb mérési periódusok
- Analyzer modul, ami eldönti: van-e forgalom, vagy csak zaj
- Grafikus waterfall megjelenítés (matplotlib)

## Fejlesztés
A kód jelenleg Pythonban készül a gyors prototípus miatt.
Később megfontolható a C++-os implementáció a `librtlsdr` és `sqlite3` közvetlen használatával,
ha nagyobb teljesítményre vagy alacsonyabb erőforrásigényre lesz szükség.

---

## Licenc
MIT
