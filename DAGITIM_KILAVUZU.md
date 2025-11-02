╔════════════════════════════════════════════════════════════════╗
║                 ETİKET YÖNETİMİ PROGRAMI                       ║
║                    Kurulum Talimatları                         ║
╚════════════════════════════════════════════════════════════════╝

📦 KURULUM ADIMLARI
-------------------

1. ZIP dosyasını bir klasöre çıkartın
   Örnek: C:\EtiketYonetimi\

2. ÖNEMLI: credentials.json dosyasını ekleyin!

   ⚠️ Program çalışmak için credentials.json gerektirir!

   Dosya yapısı şöyle olmalı:

   C:\EtiketYonetimi\
   ├── EtiketYonetimi.exe
   ├── credentials.json        ← SİZ EKLEYİN!
   ├── etiketEkle.json
   └── Etiket.gsheet

3. EtiketYonetimi.exe'yi çift tıklayın

4. İlk çalıştırmada:
   - Tarayıcı açılacak
   - Google hesabınızla giriş yapın
   - İzin verin
   - token.pickle dosyası oluşacak (yedekleyin!)

5. Artık programı kullanabilirsiniz!


🔑 CREDENTIALS.JSON NEREDEN ALINIR?
------------------------------------

1. Google Cloud Console'a gidin:
   https://console.cloud.google.com/

2. Yeni proje oluşturun veya mevcut projeyi seçin

3. APIs & Services > Credentials

4. CREATE CREDENTIALS > OAuth client ID

5. Application type: Desktop app

6. Dosyayı indirin ve "credentials.json" olarak kaydedin

7. credentials.json'u program klasörüne kopyalayın


⚠️ HATA: "credentials.json BULUNAMADI"
---------------------------------------

Bu hatayı alırsanız:

1. credentials.json dosyasının .exe ile AYNI klasörde olduğundan
   emin olun

2. Dosya adının tam olarak "credentials.json" olduğunu kontrol edin
   (büyük/küçük harf önemli!)

3. Dosyanın içeriğinin JSON formatında olduğunu kontrol edin


📞 YARDIM
---------

Sorun yaşarsanız:
1. credentials.json'u doğru klasöre koyduğunuzdan emin olun
2. Programı Yönetici olarak çalıştırmayı deneyin
3. Windows Defender'ı geçici olarak kapatıp deneyin


✅ BAŞARILI KURULUM
-------------------

Program başarıyla açılırsa:
- ✅ credentials.json doğru yerde
- ✅ Google Sheets bağlantısı çalışıyor
- ✅ Her şey hazır!

İyi çalışmalar!
