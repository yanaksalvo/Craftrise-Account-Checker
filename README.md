# Craftrise Account Checker

Bu proje, Craftrise hesaplarını kontrol etmek için geliştirilmiş bir Python tabanlı araçtır. Kullanıcı adı ve şifre kombinasyonlarını kontrol ederek RC, Mail, Klan gibi bilgileri döndürür.

## Gereksinimler

- **Python**: Sisteminizde Python 3.x yüklü olmalıdır. [Python İndirme](https://www.python.org/downloads/)
- Gerekli Python modülleri (aşağıda açıklanmıştır).

## Kurulum

1. **Python Kurulumu**  
   Sisteminizde Python yüklü değilse, yukarıdaki linkten indirip kurun.

2. **Gerekli Modülleri Yükleme**  
   Projenin çalışması için gerekli modülleri yüklemek için terminalde aşağıdaki komutu çalıştırın:
   *Not: Eğer `requirements.txt` dosyası yoksa, projede kullanılan modülleri manuel olarak yüklemeniz gerekebilir.*

3. **Proje Dosyalarını İndirin**  
   Bu depoyu klonlayın veya ZIP olarak indirip çıkarın:
   ```bash
   git clone https://github.com/yanaksalvo/Craftrise-Account-Checker.git
   ```

## Kullanım

1. **Cloudflare Turnstile Token Çekme**  
   - Terminali açın ve aşağıdaki komutu çalıştırarak `cfbp.py` dosyasını başlatın:
     ```bash
     py cfbp.py
     ```
     Bu dosya, Craftrise sitesindeki Cloudflare Turnstile tokenini çeker ve API şeklinde çalışır. Bu işlem sürekli açık kalmalıdır, çünkü her kontrolde yeni bir token gereklidir.

2. **Hesap Bilgilerini Hazırlama**  
   - `sa.txt` dosyasını açın ve kontrol etmek istediğiniz Craftrise hesaplarını `kullanıcı_adı:şifre` formatında her satıra bir hesap olacak şekilde ekleyin. Örnek:
     ```
     kullanici1:sifre1
     kullanici2:sifre2
     ```

3. **Kontrol İşlemini Başlatma**  
   - Yeni bir terminal açın ve aşağıdaki komutu çalıştırın:
     ```bash
     py check.py
     ```
     Bu komut, hesap kontrol işlemini başlatır. Başarılı bir şekilde çalıştığında, RC, Mail, Klan gibi bilgileri döndürecektir.

## Notlar

- `cfbp.py` dosyasının sürekli çalışır durumda olması gerektiğini unutmayın.
- `sa.txt` dosyasına eklediğiniz hesap bilgilerinin doğru formatta olduğundan emin olun.
- Herhangi bir hata veya sorunla karşılaşırsanız, terminaldeki hata mesajlarını kontrol edin veya sorun bildirin.



## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## İletişim

https://t.me/babakonusmazgosterirhepicraat
