import requests
from bs4 import BeautifulSoup
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BROWSERLESS_TOKEN = os.getenv("BROWSERLESS_TOKEN")
BROWSERLESS_API = "https://chrome.browserless.io/content?token=" + BROWSERLESS_TOKEN + "&url="

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def check_subtitles(url):
    try:
        print(f"Kiểm tra: {url}")
        full_url = BROWSERLESS_API + url
        r = requests.get(full_url, timeout=60)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text().lower()
        if "vietnamese" in text or "tiếng việt" in text:
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
            time.sleep(2)  # tránh gửi dồn dập
    if found:
        message = "🎉 Có phụ đề <b>Vietnamese</b> mới!\n\n" + "\n".join(found)
        send_telegram(message)
    else:
        print("Không có phụ đề mới nào.")

if __name__ == "__main__":
    main()
