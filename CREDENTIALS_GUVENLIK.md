# 🔒 Credentials.json Güvenlik Rehberi

## 📋 İçindekiler
1. [Harici Dosya (Önerilen)](#çözüm-1-harici-dosya-önerilen)
2. [Şifreli Dahil Etme](#çözüm-2-şifreli-dahil-etme)
3. [Çevresel Değişkenler](#çözüm-3-çevresel-değişkenler)
4. [Karşılaştırma Tablosu](#karşılaştırma-tablosu)

---

## 🎯 Çözüm 1: Harici Dosya (ÖNERİLEN)

### ✅ Avantajlar
- ✅ En güvenli yöntem
- ✅ .exe içinde hassas bilgi yok
- ✅ Her kullanıcı kendi credentials'ını kullanabilir
- ✅ Güncelleme kolay (.exe yeniden build gerekmez)

### ❌ Dezavantajlar
- ❌ Kullanıcı credentials.json'ı manuel eklemeli
- ❌ Dosya eksikse program çalışmaz

### 📝 Uygulama

**Yapılandırma (Zaten Yapıldı):**

1. **build_exe.spec** - credentials.json hariç tutuldu:
```python
datas = [
    (str(project_dir / 'config.py'), '.'),
    # (str(project_dir / 'credentials.json'), '.'),  # DIŞARIDA
    (str(project_dir / 'etiketEkle.json'), '.'),
]
```

2. **credentials_helper.py** - Dosya kontrolü eklendi:
```python
def check_credentials_file():
    """Credentials.json'ı kontrol eder"""
    creds_path = find_credentials_file()
    if not creds_path:
        return False, "credentials.json BULUNAMADI!"
    return True, "OK"
```

3. **run.py** - Başlangıçta kontrol:
```python
success, message = check_credentials_file()
if not success:
    # Hata göster ve çık
    error_dialog.setDetailedText(message)
    sys.exit(1)
```

### 📦 Dağıtım Yapısı
```
dist/
├── EtiketYonetimi.exe
├── credentials.json           ← Kullanıcı ekleyecek
├── DAGITIM_KILAVUZU.md
└── credentials.json.BURAYA_KOYUN.txt
```

---

## 🔐 Çözüm 2: Şifreli Dahil Etme

### ✅ Avantajlar
- ✅ Kullanıcı credentials.json eklemeye gerek yok
- ✅ Tek dosya (.exe) dağıtımı mümkün
- ✅ Çalışması garanti

### ❌ Dezavantajlar
- ❌ Orta seviye güvenlik
- ❌ Her kullanıcı aynı credentials kullanır
- ❌ Güncelleme için .exe yeniden build gerekir
- ❌ Şifre çözme kodu .exe içinde görülebilir

### 📝 Uygulama

**1. Şifreleme Modülü Oluşturun:**

```python
# credentials_crypto.py
from cryptography.fernet import Fernet
import base64
import json

# Sabit şifre anahtarı (değiştirin!)
KEY = b'YOUR_SECRET_KEY_HERE_32_BYTES_LONG=='

def encrypt_credentials(input_file, output_file):
    """credentials.json'ı şifreler"""
    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(KEY)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

    print(f"[OK] Şifrelendi: {output_file}")

def decrypt_credentials():
    """Şifreli credentials.json'ı çözer"""
    try:
        with open('credentials.encrypted', 'rb') as f:
            encrypted = f.read()

        fernet = Fernet(KEY)
        decrypted = fernet.decrypt(encrypted)

        return json.loads(decrypted)
    except Exception as e:
        print(f"[ERROR] Şifre çözme hatası: {e}")
        return None

# Kullanım (build öncesi):
if __name__ == "__main__":
    encrypt_credentials('credentials.json', 'credentials.encrypted')
```

**2. build_exe.spec'i güncelleyin:**
```python
datas = [
    (str(project_dir / 'credentials.encrypted'), '.'),  # Şifreli dahil
]
```

**3. run.py'de kullanın:**
```python
from credentials_crypto import decrypt_credentials

# Başlangıçta
credentials = decrypt_credentials()
if not credentials:
    print("Credentials çözülemedi!")
    sys.exit(1)
```

**Gerekli Paket:**
```bash
pip install cryptography
```

---

## 🌍 Çözüm 3: Çevresel Değişkenler

### ✅ Avantajlar
- ✅ .exe içinde hiçbir hassas bilgi yok
- ✅ Sunucu/Kurumsal ortamlar için ideal
- ✅ Merkezi yönetim mümkün

### ❌ Dezavantajlar
- ❌ Normal kullanıcılar için karmaşık
- ❌ Her bilgisayarda environment setup gerekir
- ❌ JSON yapısı için uygun değil (çok fazla değişken)

### 📝 Uygulama

**1. Çevresel Değişken Modülü:**

```python
# credentials_env.py
import os
import json

def load_credentials_from_env():
    """Environment variables'dan credentials oluştur"""

    # Yöntem 1: JSON string olarak
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if creds_json:
        return json.loads(creds_json)

    # Yöntem 2: Dosya yolu
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
    if creds_path and os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            return json.load(f)

    # Yöntem 3: Ayrı ayrı değişkenler
    return {
        "installed": {
            "client_id": os.getenv('GOOGLE_CLIENT_ID'),
            "project_id": os.getenv('GOOGLE_PROJECT_ID'),
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
            # ... diğer alanlar
        }
    }

# Kullanım
credentials = load_credentials_from_env()
```

**2. Windows'da Environment Variable Ayarlama:**

```batch
REM Yönetici CMD'de
setx GOOGLE_CREDENTIALS_PATH "C:\Secrets\credentials.json" /M

REM veya

setx GOOGLE_CREDENTIALS_JSON "{\"installed\":{...}}" /M
```

**3. run.py'de kullanın:**
```python
from credentials_env import load_credentials_from_env

credentials = load_credentials_from_env()
if not credentials or not credentials.get('installed'):
    print("Environment variables eksik!")
    sys.exit(1)
```

---

## 📊 Karşılaştırma Tablosu

| Özellik | Harici Dosya | Şifreli Dahil | Env Variables |
|---------|--------------|---------------|---------------|
| **Güvenlik** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Kullanım Kolaylığı** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Dağıtım Kolaylığı** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Bakım Kolaylığı** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Çoklu Kullanıcı** | ✅ | ❌ | ✅ |
| **Güncelleme** | Kolay | Zor | Orta |
| **Setup Zamanı** | Orta | Hızlı | Yavaş |

---

## 💡 Öneri: Hibrit Yaklaşım

En iyi çözüm: **Üç yöntemi birden desteklemek!**

```python
# credentials_manager.py
def get_credentials():
    """Credentials'ı öncelik sırasına göre bul"""

    # 1. Environment variables'ı dene
    creds = load_credentials_from_env()
    if creds:
        print("[OK] Credentials environment'tan yüklendi")
        return creds

    # 2. Harici dosyayı dene
    creds_path = find_credentials_file()
    if creds_path:
        with open(creds_path, 'r') as f:
            print(f"[OK] Credentials dosyadan yüklendi: {creds_path}")
            return json.load(f)

    # 3. Şifreli dahili dosyayı dene
    creds = decrypt_credentials()
    if creds:
        print("[OK] Credentials dahili şifreli dosyadan yüklendi")
        return creds

    # Hiçbiri bulunamadı
    return None
```

---

## 🎯 Hangi Yöntemi Seçmeliyim?

### Ev/Küçük İşletme Kullanımı
→ **Harici Dosya** (Çözüm 1) - Zaten uygulandı!

### Tek Kullanıcı/Kolay Dağıtım
→ **Şifreli Dahil** (Çözüm 2)

### Kurumsal/Sunucu Ortamı
→ **Environment Variables** (Çözüm 3)

### Geniş Kullanıcı Tabanı
→ **Hibrit Yaklaşım** (Hepsi)

---

## 📝 Şu An Aktif Olan Çözüm

✅ **Çözüm 1: Harici Dosya** - Uygulandı ve çalışıyor!

Program şu anda:
1. credentials.json'ı .exe'nin yanında arar
2. Bulamazsa kullanıcıya detaylı hata mesajı gösterir
3. Kullanıcı credentials.json'ı doğru klasöre koyar
4. Program çalışır

---

## 🔄 Başka Bir Çözüme Geçmek İsterseniz

### Şifreli Dahil'e geçiş:
```bash
# 1. Şifreleme kodunu ekleyin
# 2. credentials.encrypted oluşturun
# 3. build_exe.spec'i güncelleyin
# 4. build.bat çalıştırın
```

### Environment Variables'a geçiş:
```bash
# 1. credentials_env.py ekleyin
# 2. run.py'yi güncelleyin
# 3. Her bilgisayarda env vars ayarlayın
```

---

**Güvenlik Notu:** Hiçbir yöntem %100 güvenli değildir. En güvenli yöntem, credentials.json'ı hiçbir şekilde paylaşmamak ve her kullanıcının kendi credentials'ını oluşturmasını sağlamaktır.

**Tavsiye:** Şu anki "Harici Dosya" yöntemi çoğu kullanım senaryosu için yeterli ve en güvenli seçenektir. Değiştirmeyin! 😊
