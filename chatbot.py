import requests
import re
import json
import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ---------------- CONFIG & STATE ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:latest" 
SCOPES = ['https://www.googleapis.com/auth/calendar']

state = "idle"
appointment_data = {}
last_appointment = None  # kullanıcıya bilgi vermek için

# ---------------- DOSYA YÜKLE ----------------
def load_file(name):
    try:
        with open(name, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

faq_content = load_file("faq.txt")
prices_content = load_file("prices.json")
biz_info = load_file("business_info.json")

# ---------------- GOOGLE CALENDAR ----------------

def get_calendar_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("HATA: credentials.json yok!")
                return None

            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def is_slot_busy(date_str, time_str):
    service = get_calendar_service()
    if not service:
        return True

    start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + datetime.timedelta(hours=1)

    events = service.events().list(
        calendarId='primary',
        timeMin=start_dt.isoformat() + 'Z',
        timeMax=end_dt.isoformat() + 'Z',
        singleEvents=True
    ).execute().get('items', [])

    return len(events) > 0

def create_event(date_str, time_str, service_name="Genel Bakım"):
    global last_appointment

    service = get_calendar_service()

    start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + datetime.timedelta(hours=1)

    event = {
        'summary': f'Nida Kuaför: {service_name}',
        'description': 'WhatsApp üzerinden alınan otomatik randevu.',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Europe/Istanbul'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Europe/Istanbul'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    last_appointment = f"{date_str} {time_str}"
    return event.get('htmlLink')

# ---------------- LLM ----------------

def ask_llm(user_input, system_context=""):
    prompt = f"""
Sen Düzce'deki Nida Bayan Kuaförü'nün asistanı Selin'sin.

KURALLAR:
- Sadece TÜRKÇE konuş
- Kısa, net ve WhatsApp tarzı yaz
- Asla "dosyaya bak" deme
- Fiyat sorulursa direkt fiyat söyle
- Konum sorulursa direkt adres söyle
- Uydurma bilgi verme

BİLGİLER:
{biz_info}
{prices_content}
{faq_content}

DURUM:
{system_context}

Kullanıcı: {user_input}
Selin:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False}
        )
        return response.json().get("response", "Canım tekrar söyler misin?")
    except:
        return "Ollama çalışmıyor gibi, bir kontrol eder misin?"

# ---------------- PARSER ----------------

def parse_date(text):
    today = datetime.date.today()
    text = text.lower()

    if "bugün" in text:
        return today.strftime("%Y-%m-%d")

    if "yarın" in text:
        return (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return None

def parse_time(text):
    match = re.search(r'(\d{1,2})', text)

    if match:
        hour = int(match.group(1))

        if hour < 0 or hour > 23:
            return None

        if "akşam" in text.lower() and hour < 12:
            hour += 12

        return f"{hour:02d}:00"

    return None

# ---------------- MAIN ----------------

def main():
    global state, appointment_data

    print("Nida Kuaför Selin aktif 💇‍♀️ (exit ile çık)\n")

    while True:
        user_input = input("Müşteri: ")

        if user_input.lower() == "exit":
            break

        # ekstra soru: randevu neydi
        if "ne randevusu" in user_input.lower() or "hangi randevu" in user_input.lower():
            if last_appointment:
                print(f"Selin: Canım {last_appointment} için randevun var ❤️")
            else:
                print("Selin: Henüz bir randevun görünmüyor canım")
            continue

        # ---------------- IDLE ----------------
        if state == "idle":

            if "randevu" in user_input.lower():
                p_date = parse_date(user_input)
                p_time = parse_time(user_input)

                if p_date:
                    appointment_data["date"] = p_date

                if p_time:
                    appointment_data["time"] = p_time

                if "date" not in appointment_data:
                    state = "waiting_date"
                    print("Selin: Hangi gün için istiyorsun canım?")
                    continue

                if "time" not in appointment_data:
                    state = "waiting_time"
                    print("Selin: Saat kaçta olsun?")
                    continue

                state = "waiting_time"

            else:
                print("Selin:", ask_llm(user_input))
                continue

        # ---------------- DATE ----------------
        if state == "waiting_date":
            p_date = parse_date(user_input)

            if not p_date:
                print("Selin: Bugün mü yarın mı canım?")
                continue

            appointment_data["date"] = p_date
            state = "waiting_time"
            print("Selin: Saat kaçta olsun?")
            continue

        # ---------------- TIME ----------------
        if state == "waiting_time":

            p_time = parse_time(user_input)

            if not p_time:
                print("Selin: Saati anlayamadım canım (örn: 14 veya akşam 6)")
                continue

            if is_slot_busy(appointment_data["date"], p_time):
                print("Selin: O saat dolu canım 😔 başka saat söyle")
                continue

            link = create_event(appointment_data["date"], p_time)

            print(f"Selin: Tamamdır ❤️ {p_time} için randevun hazır!")
            print(f"(Link: {link})")

            state = "idle"
            appointment_data = {}

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()