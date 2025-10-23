import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def check_subtitles(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Tìm các phụ đề, có thể cần điều chỉnh nếu cấu trúc web thay đổi
        subtitles = [a.get_text(strip=True) for a in soup.find_all("a")]

        for sub in subtitles:
            if "vietnamese" in sub.lower() or "tiếng việt" in sub.lower():
                return True
        return False
    except Exception as e:
        print(f"Lỗi khi truy cập {url}: {e}")
        return False

def main():
    with open("list.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    found = []
    for link in links:
        if check_subtitles(link):
            found.append(link)

    if found:
        message = "🎉 Có phụ đề <b>Vietnamese</b> mới!\n\n" + "\n".join(found)
        send_telegram(message)
    else:
        print("Không có phụ đề mới nào.")

if __name__ == "__main__":
    main()
