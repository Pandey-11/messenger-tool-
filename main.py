import requests
import json
import time
import os

def logo():
    os.system("clear")
    print("\033[1;32m")
    print(" <3 :D NIKHIL PAPA :D <3")
    print("=========================================")
    print("   <3 8| BL4CK W4RRI0R RULL3X H3R3 8| <3")
    print("=========================================\033[0m\n")

def send_message(session, uid, message):
    url = f"https://www.facebook.com/messages/t/{uid}"
    data = {
        "message": message,
        "tids": uid
    }
    response = session.post(url, data=data)
    if response.status_code == 200:
        print(f"[✓] Message sent: {message}")
    else:
        print(f"[x] Error: {response.status_code} | {response.text}")

def main():
    logo()

    print("[1] Login using Appstate JSON")
    print("[2] Login using Normal Cookies (c_user + xs)")
    choice = input("\n[?] Choose login method (1/2): ")

    session = requests.Session()

    if choice.strip() == "1":
        appstate = input("\n[?] Paste Your Appstate JSON: ")
        appstate = json.loads(appstate)
        cookies = {}
        for item in appstate:
            cookies[item['key']] = item['value']
        session.cookies.update(cookies)

    elif choice.strip() == "2":
        c_user = input("\n[?] Enter c_user: ").strip()
        xs = input("[?] Enter xs: ").strip()
        cookies = {
            "c_user": c_user,
            "xs": xs
        }
        session.cookies.update(cookies)

    else:
        print("[x] Invalid choice!")
        return

    # Conversation UID
    uid = input("\n[?] Enter Target UID: ")

    # Messages file path
    message_file = input("\n[?] Enter your message file path (e.g. messages.txt): ").strip()
    if not os.path.exists(message_file):
        print(f"[x] File not found: {message_file}")
        return

    with open(message_file, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        print("[x] No messages found in file!")
        return

    # Delay
    delay = int(input("\n[?] Enter delay in seconds: "))

    # Start sending
    print("\n[+] Starting message sender...\n")
    for message in messages:
        send_message(session, uid, message)
        time.sleep(delay)

if __name__ == "__main__":
    main()
