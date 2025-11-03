# 📦 Etiket Yönetimi - EXE Paketleme Rehberi

## 🚀 Hızlı Başlangıç

### 1. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. EXE Oluşturun

**Kolay Yol (Otomatik):**
```bash
build.bat
```

**Manuel Yol:**
```bash
pyinstaller --clean build_exe.spec
```

### 3. EXE'yi Test Edin

```bash
cd dist
EtiketYonetimi.exe
```

---

## 📁 Dosya Yapısı

### Kaynak Dosyalar
```
d:\GoogleDrive\Fiyat\Etiket\
│
├── run.py                  # Ana başlatma
├── config.py               # Yapılandırma
├── jsonGoster.py           # UI modülü
├── etiketEkle.py           # Etiket ekleme
├── etiketYazdir.py         # PDF yazdırma
├── dogtasCom.py            # Web scraper
│
├── credentials.json        # Google OAuth (GİZLİ!)
├── etiketEkle.json         # Veri dosyası
├── Etiket.gsheet           # Sheets kısayol
│
├── build_exe.spec          # PyInstaller config
├── build.bat               # Build scripti
├── requirements.txt        # Python paketleri
└── .gitignore              # Git ignore dosyası
```

### Oluşturulan Dosyalar
```
dist\
└── EtiketYonetimi.exe      # Çalıştırılabilir dosya

build\                      # Geçici dosyalar (silinebilir)
```

---

## ⚙️ Build Seçenekleri

### Tek Dosya (--onefile)
**Avantaj:** Tek bir .exe dosyası
**Dezavantaj:** Daha yavaş başlatma
**Boyut:** ~50-70 MB

```python
# build_exe.spec içinde:
exe = EXE(
    ...
    name='EtiketYonetimi',
    onefile=True,  # Ekleyin
)
---

## 🔧 Özelleştirmeler

### İkon Eklemek

1. Bir .ico dosyası hazırlayın (örn: `icon.ico`)
2. `build_exe.spec` dosyasını düzenleyin:

```python
exe = EXE(
    ...
    icon='icon.ico',  # İkon dosyası
)
```

### Konsol Penceresini Göstermek (Debug için)

```python
exe = EXE(
    ...
    console=True,  # True yapın
)
```

### Dosya Boyutunu Küçültmek

```python
# build_exe.spec içinde excludes listesine ekleyin:
excludes=[
    'matplotlib',
    'numpy.testing',
    'tkinter',
    'unittest',
    'email',
    'http',
    'xml',
]
```

---

## 📤 Dağıtım

### Başka Bilgisayarda Çalıştırmak

**Seçenek 1: Tek Dosya Modu (--onefile)**
- Sadece `EtiketYonetimi.exe` dosyasını kopyalayın
- Python yüklü olmasına gerek YOK

**Seçenek 2: Klasör Modu (--onedir) - ÖNERİLEN**
- `dist` klasörünün içindeki **TÜM DOSYALARI** kopyalayın
- Ana .exe dosyası ile birlikte _internal klasörü de gerekli
- Python yüklü olmasına gerek YOK

### ⚠️ Önemli Notlar

1. **Antivirüs Uyarısı:**
   - Bazı antivirüsler PyInstaller .exe'lerini şüpheli bulabilir
   - Windows Defender → İzin Verilenler'e ekleyin

2. **Credentials.json:**
   - Bu dosya Google OAuth kimlik bilgilerini içerir
   - EXE içinde paketlenmiştir
   - Hassas bilgi içerir, dikkatli paylaşın

3. **İlk Çalıştırma:**
   - Google OAuth için tarayıcı açılabilir
   - `token.pickle` dosyası oluşturulacak
   - Bu dosyayı yedekleyin (yeniden giriş yapmamak için)

4. **Güncellemeler:**
   - Kaynak kodda değişiklik yaparsanız
   - `build.bat` dosyasını tekrar çalıştırın

---

## 🐛 Sorun Giderme

### "ModuleNotFoundError" Hatası

**Çözüm:** `hiddenimports` listesine eksiği ekleyin:

```python
hiddenimports = [
    'PyQt5.QtCore',
    'eksik_modul_adi',  # Buraya ekleyin
]
```

### "FileNotFoundError: credentials.json"

**Çözüm:** `datas` listesinde dosya yolu doğru olmalı:

```python
datas = [
    ('credentials.json', '.'),
]
```

### EXE Çok Büyük

**Çözüm 1:** Gereksiz paketleri exclude edin
**Çözüm 2:** UPX ile sıkıştırın (otomatik)
**Çözüm 3:** Virtual environment kullanın

---

## ✅ Başarılı Build Kontrolü

Build sonrası şunları kontrol edin:

- [x] `dist\EtiketYonetimi.exe` oluştu mu?
- [x] .exe çalıştırıldığında konsol açılmıyor mu?
- [x] Program penceresi açılıyor mu?
- [x] Google Sheets bağlantısı çalışıyor mu?
- [x] PDF oluşturma fonksiyonu çalışıyor mu?

---

## 📞 Yardım

Sorun yaşarsanız:
1. `build.bat` çıktısını kontrol edin
2. `build\EtiketYonetimi\warn-EtiketYonetimi.txt` dosyasını inceleyin
3. Console modunda çalıştırıp hataları görün (`console=True`)

---

**Son Güncelleme:** Kasım 2025
**PyInstaller Versiyonu:** 5.0+
**Python Versiyonu:** 3.13
