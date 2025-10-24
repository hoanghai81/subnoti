import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("SUBSOURCE_API_KEY")

API_BASE = "https://api.subsource.net/api/v1"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("❌ Telegram error:", e)

def check_movie(imdb_id, title):
    url = f"{API_BASE}/subtitles?imdbId={imdb_id}&language=vietnamese"
    headers = {"X-API-Key": API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("data"):
            print(f"✅ Có phụ đề Vietnamese cho {title}")
            return True
        else:
            print(f"❌ Chưa có phụ đề Vietnamese cho {title}")
            return False
    except Exception as e:
        print(f"⚠️ Lỗi khi kiểm tra {title}: {e}")
        return False

def main():
    found = []
    with open("list.txt", "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            # Format: imdbId|Tên phim
            try:
                imdb_id, title = line.strip().split("|", 1)
            except ValueError:
                print("⚠️ Sai định dạng dòng:", line)
                continue
            if check_movie(imdb_id.strip(), title.strip()):
                found.append(f"{title} ({imdb_id})")
            time.sleep(1)

    if found:
        msg = "🎬 <b>Phụ đề Vietnamese mới có:</b>\n" + "\n".join(f"• {x}" for x in found)
        send_telegram(msg)
    else:
        print("Không có phụ đề mới nào.")

if __name__ == "__main__":
    main()
