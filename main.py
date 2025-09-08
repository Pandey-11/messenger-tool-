import requests
import re
import time
import os
import json

def logo():
    os.system("clear")
    print("\033[1;32m")
    print(" <3 :D NIKHIL PAPA :D <3")
    print("=========================================")
    print("   <3 8| BL4CK W4RRI0R RULL3X H3R3 8| <3")
    print("=========================================\033[0m\n")

def parse_cookie_string(raw_cookie):
    cookies = {}
    parts = raw_cookie.split(";")
    for part in parts:
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k.strip()] = v.strip()
    return cookies

def get_tokens(session):
    r = session.get("https://mbasic.facebook.com/")
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', r.text).group(1)
    jazoest = re.search(r'name="jazoest" value="(.*?)"', r.text).group(1)
    return fb_dtsg, jazoest

def send_message(session, fb_dtsg, jazoest, uid, message):
    url = "https://www.facebook.com/api/graphql/"
    data = {
        "av": session.cookies.get("c_user"),
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
        "doc_id": "3844807015600800",  # Messenger SendMessageMutation
        "variables": f'{{"message":{{"text":"{message}"}},"recipient":{{"id":"{uid}"}}}}'
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) Chrome/118.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = session.post(url, data=data, headers=headers)
    if r.status_code == 200 and "errors" not in r.text:
        print(f"[✓] Message sent: {message}")
    else:
        print(f"[x] Failed: {r.text[:200]}...")

def main():
    logo()
    print("[1] Login using Fbstate (Appstate JSON)")
    print("[2] Login using Raw Cookie String (Monotoolkit format)")
    choice = input("\n[?] Choose login method (1/2): ").strip()

    session = requests.Session()

    if choice == "1":
        fbstate = input("\n[?] Paste your Fbstate JSON: ").strip()
        try:
            fbstate = json.loads(fbstate)
            cookies = {}
            for item in fbstate:
                cookies[item["key"]] = item["value"]
            session.cookies.update(cookies)
        except Exception as e:
            print(f"[x] Invalid Fbstate JSON! {e}")
            return

    elif choice == "2":
        raw_cookie = input("\n[?] Paste your full raw cookie string: ").strip()
        cookies = parse_cookie_string(raw_cookie)
        session.cookies.update(cookies)

    else:
        print("[x] Invalid choice!")
        return

    uid = input("\n[?] Enter Target UID: ").strip()
    message_file = input("[?] Enter message file path (e.g. messages.txt): ").strip()
    delay = int(input("[?] Enter Delay (seconds): "))

    if not os.path.exists(message_file):
        print(f"[x] File not found: {message_file}")
        return

    with open(message_file, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        print("[x] No messages found in file!")
        return

    fb_dtsg, jazoest = get_tokens(session)

    print("\n[+] Starting message sender...\n")
    for message in messages:
        send_message(session, fb_dtsg, jazoest, uid, message)
        time.sleep(delay)

if __name__ == "__main__":
    main()
