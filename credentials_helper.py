"""
Credentials.json Yönetim Yardımcısı
Bu modül credentials.json dosyasının varlığını kontrol eder ve kullanıcıya yardımcı olur.
"""

import os
import sys
from pathlib import Path


def get_base_dir():
    """Exe veya script dizinini döndür"""
    if getattr(sys, 'frozen', False):
        # PyInstaller ile paketlenmişse
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def find_credentials_file():
    """
    credentials.json dosyasını arar

    Returns:
        str: Dosya yolu veya None
    """
    base_dir = get_base_dir()

    # Aranacak yerler (öncelik sırasına göre)
    possible_paths = [
        os.path.join(base_dir, 'credentials.json'),  # .exe'nin yanı
        os.path.join(Path.home(), 'credentials.json'),  # Kullanıcı home
        os.path.join(base_dir, '..', 'credentials.json'),  # Bir üst dizin
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def check_credentials_file():
    """
    credentials.json dosyasını kontrol eder ve kullanıcıyı bilgilendirir

    Returns:
        tuple: (bool başarılı, str mesaj)
    """
    creds_path = find_credentials_file()

    if creds_path:
        return True, f"Credentials bulundu: {creds_path}"

    # Dosya bulunamadı - detaylı hata mesajı
    base_dir = get_base_dir()
    error_msg = f"""
╔════════════════════════════════════════════════════════════════╗
║  ⚠️  HATA: credentials.json BULUNAMADI!                        ║
╚════════════════════════════════════════════════════════════════╝

Google Sheets API için credentials.json dosyası gereklidir.

ÇÖZÜM:
------
1. credentials.json dosyanızı şu konuma kopyalayın:
   {base_dir}

2. Dosya yapısı şöyle olmalı:
   {base_dir}/
   ├── EtiketYonetimi.exe
   ├── credentials.json  ← Buraya kopyalayın
   └── etiketEkle.json

3. Programı tekrar çalıştırın.

NOT: credentials.json dosyası Google Cloud Console'dan
     indirilmiş OAuth 2.0 kimlik bilgileri içermelidir.

Yardım için: https://console.cloud.google.com/apis/credentials
"""
    return False, error_msg


def create_credentials_template():
    """
    Kullanıcı için credentials.json template'i oluşturur
    """
    base_dir = get_base_dir()
    template_path = os.path.join(base_dir, 'credentials.json.template')

    template = {
        "installed": {
            "client_id": "BURAYA_CLIENT_ID_YAZIN.apps.googleusercontent.com",
            "project_id": "BURAYA_PROJECT_ID_YAZIN",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "BURAYA_CLIENT_SECRET_YAZIN",
            "redirect_uris": ["http://localhost"]
        }
    }

    import json
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)

    return template_path


if __name__ == "__main__":
    # Test için
    success, message = check_credentials_file()
    print(message)

    if not success:
        print("\n[INFO] Template oluşturuluyor...")
        template_path = create_credentials_template()
        print(f"[OK] Template oluşturuldu: {template_path}")
        print("[INFO] Template dosyasını doldurup credentials.json olarak kaydedin")
