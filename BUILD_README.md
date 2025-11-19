# 📦 Etiket Programı - EXE Oluşturma Kılavuzu

## 🚀 Hızlı Başlangıç

### Yöntem 1: Otomatik Build (Önerilen)
Sadece `BUILD.bat` dosyasına çift tıklayın. Tüm işlemler otomatik yapılacak!

### Yöntem 2: Manuel Build
1. Terminal/CMD açın
2. Şu komutu çalıştırın:
```bash
cd D:\GoogleDrive\Fiyat\Etiket
python build_exe.py
```

## 📋 Gereksinimler
- Python 3.8 veya üzeri
- Tüm paketler otomatik yüklenecek

## 📁 Çıktı
Build tamamlandığında `dist` klasöründe şu dosyalar olacak:
- **EtiketProgrami.exe** - Ana GUI programı (konsol açılmaz)
- **dogtasCom.exe** - Web scraper (konsol açılmaz)
- **etiketEkle.json** - Veri dosyası
- **service-account.json** - Google Sheets kimlik dosyası
- **icon.ico** - Program ikonu

## ✅ Özellikler
✓ Konsol penceresi açılmaz (windowed mode)
✓ Tüm Python paketleri dahil
✓ Tek exe dosyası (onefile mode)
✓ Her bilgisayarda çalışır (Python gerektirmez)
✓ Taşınabilir (USB'ye kopyalayıp çalıştırabilirsiniz)

## 🎯 Kullanım
1. `dist` klasöründeki tüm dosyaları istediğiniz yere kopyalayın
2. `EtiketProgrami.exe` dosyasına çift tıklayın
3. Program açılacak, konsol penceresi AÇILMAYACAK

## 🔧 Sorun Giderme
**Problem:** "PyInstaller bulunamadı" hatası
**Çözüm:** `pip install pyinstaller` komutunu çalıştırın

**Problem:** Bazı paketler eksik
**Çözüm:** `pip install -r requirements.txt` komutunu çalıştırın

**Problem:** Build başarısız
**Çözüm:** `build_exe.py` dosyasını düzenleyin ve hata mesajını kontrol edin

## 📞 Destek
Herhangi bir sorun yaşarsanız:
1. `dogtasCom.log` dosyasını kontrol edin
2. Terminal'de hata mesajlarını okuyun
3. Build sırasında çıkan tüm mesajları kaydedin
