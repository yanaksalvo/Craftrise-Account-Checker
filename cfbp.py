from flask import Flask, jsonify
from DrissionPage import ChromiumPage
import time
import subprocess

app = Flask(__name__)
page = ChromiumPage()
widget_id = None

# Token hata sayacı
token_failures = 0

# WARP'ı yeniden başlatan fonksiyon
def restart_warp():
    try:
        print("\U0001f501 WARP yeniden başlatılıyor...")
        subprocess.run(["warp-cli", "disconnect"], check=True)
        time.sleep(3)
        subprocess.run(["warp-cli", "connect"], check=True)
        print("\u2705 WARP bağlantısı yeniden kuruldu.")
    except Exception as e:
        print(f"\u274c WARP yeniden başlatılamadı: {e}")


def initialize_page():
    print("Sayfa açılıyor...")
    page.get('https://www.craftrise.com.tr')
    time.sleep(3)

    js = """
    const div = document.createElement('div');
    div.id = 'captcha-container';
    document.body.appendChild(div);

    const script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);

    script.onload = () => {
        const id = turnstile.render('#captcha-container', {
            sitekey: '0x4AAAAAAA4cK60wpgOTyti9',
            callback: function(token) {
                window._cf_token = token;
                console.log('New token:', token);
            }
        });
        window._cf_widget_id = id;
    };
    """
    page.run_js(js)

    print("Turnstile yükleniyor...")
    for _ in range(20):
        has_token = page.run_js('return window._cf_token !== undefined')
        has_widget = page.run_js('return window._cf_widget_id !== undefined')
        if has_token and has_widget:
            print("Başlangıç token ve widget ID hazır.")
            return True
        time.sleep(1)

    print("Başlangıçta token veya widget ID alınamadı.")
    return False


@app.route('/get-token', methods=['GET'])
def get_new_token():
    global token_failures
    try:
        page.run_js("turnstile.reset(window._cf_widget_id);")
        print("\U0001f501 Token yenileniyor...")

        for _ in range(10):
            token = page.run_js('return window._cf_token || null;')
            if token:
                token_failures = 0
                return jsonify({"token": token})
            time.sleep(1)

        print("\u26a0\ufe0f Token alınamadı.")
        token_failures += 1
        if token_failures >= 2:
            print("\ud83d\udea8 2 ardışık hata sonrası WARP resetleniyor...")
            restart_warp()
            token_failures = 0

        return jsonify({"error": "Yeni token alınamadı"}), 500

    except Exception as e:
        print(f"\u274c Token alma hatası: {e}")
        token_failures += 1
        if token_failures >= 2:
            print("\ud83d\udea8 2 ardışık exception sonrası WARP resetleniyor...")
            restart_warp()
            token_failures = 0
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return 'Her istekte yeni Turnstile token döner.'


if __name__ == '__main__':
    try:
        if not initialize_page():
            print("Sayfa başlatılamadı.")
            exit(1)
        app.run(host='0.0.0.0', port=5001)
    finally:
        page.quit()
