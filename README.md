# 🏷️ Etiket Yönetimi Sistemi

Doğtaş için geliştirilmiş etiket yönetim, fiyat karşılaştırma ve PDF üretim programı.

## 📋 Özellikler

- ✅ Google Sheets ile fiyat senkronizasyonu
- ✅ JSON tabanlı ürün veritabanı
- ✅ PyQt5 ile modern arayüz
- ✅ PDF etiket yazdırma
- ✅ Doğtaş.com web scraping
- ✅ Otomatik fiyat güncelleme
- ✅ Koleksiyon bazlı fiyat tahmini
- ✅ .EXE paketleme desteği

## 🚀 Kurulum

### Gereksinimler

- Python 3.13+
- pip

### Adımlar

1. **Repository'yi klonlayın**
```bash
git clone <repository-url>
cd Etiket
```

2. **Gerekli paketleri yükleyin**
```bash
pip install -r requirements.txt
```

3. **Google Sheets API Kurulumu**

   a. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin

   b. Yeni bir proje oluşturun

   c. APIs & Services > Library > Google Sheets API'yi etkinleştirin

   d. Credentials > Create Credentials > OAuth client ID

   e. Application type: Desktop app

   f. Dosyayı indirip `credentials.json` olarak kaydedin

   g. `credentials.json` dosyasını proje klasörüne kopyalayın

4. **config.py dosyasını yapılandırın**
```python
# config.py
SPREADSHEET_ID = "YOUR_GOOGLE_SHEETS_ID_HERE"
```

5. **Programı çalıştırın**
```bash
python run.py
```

## 📦 .EXE Paketleme

### Tek Komutla Paketleme

```bash
build.bat
```

### Manuel Paketleme

```bash
pip install pyinstaller
pyinstaller --clean build_exe.spec
```

Build sonrası `dist/` klasöründe .exe dosyası oluşur.

**Önemli:** credentials.json dosyası güvenlik nedeniyle .exe içine dahil edilmemiştir.
Kullanıcılar kendi credentials.json dosyalarını .exe'nin yanına kopyalamalıdır.

Detaylı talimatlar: [BUILD_README.md](BUILD_README.md)

## 📁 Dosya Yapısı

```
Etiket/
├── run.py                      # Ana başlatma dosyası
├── config.py                   # Yapılandırma
├── jsonGoster.py               # Fiyat karşılaştırma UI
├── etiketEkle.py               # Etiket ekleme modülü
├── etiketYazdir.py             # PDF yazdırma
├── dogtasCom.py                # Web scraper
├── credentials_helper.py       # Credentials yönetimi
│
├── build_exe.spec              # PyInstaller config
├── build.bat                   # Build scripti
├── requirements.txt            # Python bağımlılıkları
│
├── .gitignore                  # Git ignore kuralları
├── README.md                   # Bu dosya
├── BUILD_README.md             # Build detaylı kılavuz
├── DAGITIM_KILAVUZU.md         # Son kullanıcı kılavuzu
└── CREDENTIALS_GUVENLIK.md     # Güvenlik rehberi
```

## 🔒 Güvenlik

### Hassas Dosyalar (Git'e eklenmez)

- ❌ `credentials.json` - Google OAuth kimlik bilgileri
- ❌ `token.pickle` - OAuth token önbelleği
- ❌ `etiketEkle.json` - Müşteri verileri

Bu dosyalar `.gitignore` ile korunur.

### Credentials Yönetimi

Program üç farklı credentials yükleme yöntemini destekler:

1. **Harici Dosya** (Varsayılan - En Güvenli)
2. **Şifreli Dahili Dosya** (İsteğe bağlı)
3. **Environment Variables** (Kurumsal)

Detaylar: [CREDENTIALS_GUVENLIK.md](CREDENTIALS_GUVENLIK.md)

## 🎯 Kullanım

### 1. Fiyat Karşılaştırma

- Google Sheets'teki fiyatları JSON ile karşılaştırır
- 7 TL üzeri farkları kırmızı gösterir
- Eksik SKU'ları sarı gösterir
- Koleksiyon bazlı fiyat tahmini yapar

### 2. Etiket Yazdırma

- PDF formatında etiketler oluşturur
- Farklı etiket şablonları destekler
- Toplu yazdırma özelliği

### 3. Web Scraping

- Doğtaş.com'dan ürün bilgileri çeker
- Google Sheets'e otomatik yükler
- Async yapı ile hızlı tarama

## 🛠️ Teknolojiler

- **Python 3.13**
- **PyQt5** - GUI framework
- **gspread** - Google Sheets API
- **pandas** - Veri işleme
- **reportlab** - PDF oluşturma
- **beautifulsoup4** - Web scraping
- **aiohttp** - Async HTTP
- **PyInstaller** - .exe paketleme

## 📝 Lisans

Bu proje Doğtaş Batman için İsmail Güneş tarafından özel olarak geliştirilmiştir.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermeden önce:

1. Yeni bir branch oluşturun
2. Değişikliklerinizi yapın
3. Test edin
4. Pull request açın

## 📞 Destek

Sorun yaşarsanız:
- Issue açın
- Dokümantasyonu okuyun: [BUILD_README.md](BUILD_README.md)

## 📊 Proje Durumu

- ✅ Aktif Geliştirme
- ✅ Production Ready
- ✅ .EXE Dağıtımı Hazır

## 🔄 Güncellemeler

### Versiyon 2.1.0 (Kasım 2025)

- ✅ Credentials harici dosya desteği
- ✅ Koleksiyon bazlı fiyat tahmini
- ✅ Hatalı fiyatlar dialog penceresi
- ✅ Konsol çıktısı temizleme
- ✅ .EXE build otomasyonu
- ✅ Güvenlik iyileştirmeleri

---

**Not:** `credentials.json` ve `etiketEkle.json` dosyaları güvenlik ve gizlilik nedeniyle bu repository'de bulunmaz. Her kullanıcı kendi dosyalarını oluşturmalıdır.
"# etiket-yonetimi" 
"# etiket-yonetimi" 
