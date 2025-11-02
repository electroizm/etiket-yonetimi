# 🚀 GitHub'a Yükleme Rehberi

## ✅ Yüklenecek Dosyalar (GÜVENLİ)

### Python Kaynak Kodları
- ✅ `run.py` - Ana program
- ✅ `config.py` - Yapılandırma
- ✅ `jsonGoster.py` - Fiyat karşılaştırma UI
- ✅ `etiketEkle.py` - Etiket ekleme
- ✅ `etiketYazdir.py` - PDF yazdırma
- ✅ `dogtasCom.py` - Web scraper
- ✅ `credentials_helper.py` - Credentials yönetimi

### Build Dosyaları
- ✅ `build_exe.spec` - PyInstaller config
- ✅ `build.bat` - Build scripti
- ✅ `requirements.txt` - Python bağımlılıkları

### Dokümantasyon
- ✅ `README.md` - Proje açıklaması
- ✅ `BUILD_README.md` - Build kılavuzu
- ✅ `DAGITIM_KILAVUZU.md` - Kullanıcı kılavuzu
- ✅ `CREDENTIALS_GUVENLIK.md` - Güvenlik rehberi

### Diğer
- ✅ `.gitignore` - Git ignore kuralları
- ✅ `Etiket.gsheet` - Google Sheets kısayol (sadece link)

## ❌ Yüklenmeyecek Dosyalar (GÜVENLİK)

### Hassas Dosyalar
- ❌ `credentials.json` - OAuth secrets (GİZLİ!)
- ❌ `token.pickle` - OAuth token (GİZLİ!)

### Veri Dosyaları
- ❌ `etiketEkle.json` - Müşteri verileri (277 KB)

### Geçici Dosyalar
- ❌ `__pycache__/` - Python cache
- ❌ `build/` - Build geçici
- ❌ `dist/` - Build çıktısı

Bu dosyalar `.gitignore` ile otomatik engellenir.

---

## 📋 Git Komutları

### 1️⃣ İlk Kurulum (Bir kez)

```bash
cd d:\GoogleDrive\Fiyat\Etiket

# Git başlat
git init

# Uzak repository ekle (GitHub'da oluşturun)
git remote add origin https://github.com/KULLANICI_ADI/etiket-yonetimi.git

# Veya SSH ile:
# git remote add origin git@github.com:KULLANICI_ADI/etiket-yonetimi.git
```

### 2️⃣ Dosyaları Ekle ve Commit Et

```bash
# Tüm güvenli dosyaları ekle (.gitignore otomatik hassas dosyaları hariç tutar)
git add .

# Commit oluştur
git commit -m "İlk commit: Etiket Yönetimi Sistemi v2.1.0

- Python kaynak kodları
- Build scriptleri
- Dokümantasyon
- .gitignore ile güvenlik
- Credentials harici dosya desteği
- Koleksiyon bazlı fiyat tahmini"

# GitHub'a yükle
git push -u origin main

# Veya master branch kullanıyorsanız:
# git push -u origin master
```

### 3️⃣ Gelecek Güncellemeler İçin

```bash
# Değişiklikleri ekle
git add .

# Commit et
git commit -m "Açıklayıcı mesaj buraya"

# GitHub'a yükle
git push
```

---

## 🔍 Yüklenmeden Önce Kontrol

### Hassas Dosyaları Kontrol Et

```bash
# Hangi dosyaların yükleneceğini göster
git status

# .gitignore'un çalıştığını doğrula
git status --ignored

# credentials.json görmemelisiniz!
```

### Yanlışlıkla Eklendiyse Kaldır

```bash
# Sadece git'ten kaldır (dosya kalır)
git rm --cached credentials.json
git rm --cached token.pickle
git rm --cached etiketEkle.json

# Commit et
git commit -m "Hassas dosyalar kaldırıldı"

# GitHub'a yükle
git push
```

---

## 🌐 GitHub Repository Oluşturma

### Adım 1: GitHub'da Yeni Repo

1. https://github.com/new adresine gidin
2. Repository name: `etiket-yonetimi`
3. Description: "Doğtaş Etiket Yönetimi Sistemi"
4. ⚠️ **Public** veya **Private** seçin (Private önerilir)
5. ❌ Initialize: README, .gitignore eklemeden
6. Create repository

### Adım 2: Yerel Repo'yu Bağla

GitHub size gösterecek komutları kullanın, örnek:

```bash
git remote add origin https://github.com/KULLANICI_ADI/etiket-yonetimi.git
git branch -M main
git push -u origin main
```

---

## 🔒 Güvenlik Kontrol Listesi

Yüklemeden önce mutlaka kontrol edin:

- [ ] `.gitignore` dosyası mevcut
- [ ] `credentials.json` **.gitignore**'da
- [ ] `token.pickle` **.gitignore**'da
- [ ] `etiketEkle.json` **.gitignore**'da
- [ ] `git status` çıktısında hassas dosya yok
- [ ] `build/` ve `dist/` klasörleri **.gitignore**'da
- [ ] Repository **Private** olarak ayarlandı (önerilir)

---

## 📊 Yüklendikten Sonra

### GitHub'da Görünecek Yapı

```
etiket-yonetimi/
├── .gitignore
├── README.md
├── BUILD_README.md
├── CREDENTIALS_GUVENLIK.md
├── DAGITIM_KILAVUZU.md
│
├── run.py
├── config.py
├── jsonGoster.py
├── etiketEkle.py
├── etiketYazdir.py
├── dogtasCom.py
├── credentials_helper.py
│
├── build_exe.spec
├── build.bat
├── requirements.txt
└── Etiket.gsheet
```

### Görünmeyecek Dosyalar (Güvenli!)

```
❌ credentials.json
❌ token.pickle
❌ etiketEkle.json
❌ __pycache__/
❌ build/
❌ dist/
```

---

## ⚠️ Önemli Uyarılar

### 1. credentials.json Asla Yüklemeyin!

Bu dosyayı yanlışlıkla yüklerseniz:

```bash
# Dosyayı geçmişten tamamen sil
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (tehlikeli, dikkatli!)
git push origin --force --all
```

### 2. Geçmiş Commit'lerde Hassas Veri Varsa

GitHub'a yükledikten sonra fark ederseniz:

1. Repository'yi SİLİN
2. Yeni repository oluşturun
3. Temiz geçmiş ile tekrar yükleyin

### 3. Private Repository Kullanın

Özellikle iş projeleri için:
- ✅ Private repository (ücretli veya ücretsiz limit dahilinde)
- ❌ Public repository (herkes görebilir)

---

## 🎯 Hızlı Başlangıç (Özet)

```bash
# 1. GitHub'da repo oluştur (Private önerilir)

# 2. Yerel dizinde:
cd d:\GoogleDrive\Fiyat\Etiket
git init
git add .
git commit -m "İlk commit: Etiket Yönetimi v2.1.0"

# 3. Remote ekle (GitHub'dan aldığınız URL)
git remote add origin https://github.com/KULLANICI_ADI/etiket-yonetimi.git

# 4. Yükle
git push -u origin main

# 5. Kontrol et
git status --ignored
```

---

## 📞 Sorun mu Yaşıyorsunuz?

### credentials.json görünüyorsa:

```bash
# .gitignore kontrol
cat .gitignore | grep credentials.json

# Çıktı olmalı: credentials.json
```

### Git user ayarları:

```bash
git config --global user.name "Adınız"
git config --global user.email "email@example.com"
```

### SSH vs HTTPS:

- **HTTPS:** Şifre ister
- **SSH:** SSH key gerekir (daha güvenli)

SSH key oluşturma: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

**Başarılar! 🎉**

Tüm hassas dosyalar `.gitignore` ile korunuyor.
Güvenle GitHub'a yükleyebilirsiniz!
