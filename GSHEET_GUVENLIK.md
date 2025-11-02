# 🔒 Etiket.gsheet Güvenlik Uyarısı

## ⚠️ SORUN

`Etiket.gsheet` dosyası GitHub'a yüklendi, ancak **hassas bilgi içeriyor**!

## 📄 Dosya İçeriği

```json
{
  "doc_id": "1-H9fA5dD9rxqcPd0VymKjMgggxUl7hAZBK0csysN-3k",
  "email": "dogtasbatman@gmail.com"
}
```

### Neler İfşa Oldu?

1. **SPREADSHEET_ID** (`doc_id`) - Google Sheets doküman kimliği
2. **Email Adresi** - Google hesap bilgisi
3. **Kimler erişebilir** - Repository'yi gören herkes

## 🛡️ RİSK SEVİYESİ

- ⚠️ **Orta Risk**: SPREADSHEET_ID ve email bilgisi açığa çıktı
- ℹ️ **İyi Haber**: Sadece ID ve email, `credentials.json` ifşa olmadı
- ✅ **Korunuyoruz**: Sheet'e erişim için OAuth credentials gerekli (o güvende)

## ✅ ÇÖZÜM

### Adım 1: `.gitignore` Güncellendi

Dosya artık `.gitignore` listesinde:

```gitignore
# Google Sheets Kısayolları - SPREADSHEET_ID ve Email İçerir
*.gsheet
Etiket.gsheet
```

### Adım 2: `build_exe.spec` Güncellendi

Dosya artık `.exe`'ye dahil edilmeyecek:

```python
datas = [
    (str(project_dir / 'config.py'), '.'),
    # (str(project_dir / 'credentials.json'), '.'),  # DIŞARIDA TUTULACAK
    (str(project_dir / 'etiketEkle.json'), '.'),
    # (str(project_dir / 'Etiket.gsheet'), '.'),  # DIŞARIDA TUTULACAK
]
```

### Adım 3: GitHub'dan Kaldırın

**Otomatik Yöntem (Kolay):**

```bash
github_gsheet_kaldir.bat
```

Bu script:
1. ✅ Dosyayı git'ten kaldırır (yerel dosyanız kalır)
2. ✅ `.gitignore` güncellemesini commit eder
3. ✅ GitHub'a yükler
4. ✅ Dosya artık repository'de görünmeyecek

**Manuel Yöntem:**

```bash
cd d:\GoogleDrive\Fiyat\Etiket

# Git'ten kaldır (yerel dosya kalır)
git rm --cached Etiket.gsheet

# Commit oluştur
git add .gitignore build_exe.spec
git commit -m "Guvenlik: Etiket.gsheet kaldirildi

- SPREADSHEET_ID ve email bilgisi iceriyordu
- .gitignore'a eklendi
- build_exe.spec'ten cikarildi"

# GitHub'a yükle
git push
```

## 🔍 Kontrol Listesi

Kaldırmadan önce:
- [x] `.gitignore` güncellendi
- [x] `build_exe.spec` güncellendi
- [ ] `git rm --cached` komutu çalıştırıldı
- [ ] Commit oluşturuldu
- [ ] GitHub'a push yapıldı

Kaldırdıktan sonra:
- [ ] GitHub repository'de dosya görünmüyor mu?
- [ ] Yerel dosyanız hala duruyor mu? (durmalı)
- [ ] Gelecek commit'lerde dosya görmüyorsunuz değil mi?

## 📋 SPREADSHEET_ID Zaten Açık mı?

Evet, `config.py` dosyasında da var:

```python
# config.py (halka açık)
SPREADSHEET_ID = "1-H9fA5dD9rxqcPd0VymKjMgggxUl7hAZBK0csysN-3k"
```

### O Zaman Neden Önemli?

1. **Email bilgisi** - `Etiket.gsheet`'te email de var, `config.py`'de yok
2. **Gereksiz tekrar** - Aynı bilgiyi iki yerde paylaşmaya gerek yok
3. **Best practice** - `.gsheet` dosyaları yerel kısayollar, paylaşılmamalı
4. **Privacy** - Email adresinizi gereksiz yere ifşa etmeyin

## 🎯 Sonuç

### Ne Yapılmalı?

1. ✅ **Script çalıştırın**: `github_gsheet_kaldir.bat`
2. ✅ **GitHub'ı kontrol edin**: Dosya görünmemeli
3. ✅ **Yerel dosyanız duruyor**: Silmeyin, kullanmaya devam edin

### Ne Olmayacak?

- ❌ Yerel dosyanız silinmeyecek
- ❌ Google Sheets erişiminiz etkilenmeyecek
- ❌ Program çalışmasına engel olmayacak

### Ne Olacak?

- ✅ Dosya GitHub'dan kaldırılacak
- ✅ Gelecekte otomatik ignore edilecek
- ✅ Email bilgisi artık görünmeyecek
- ✅ Daha güvenli olacak

---

## 📞 Sorun mu Yaşıyorsunuz?

### Dosya hala GitHub'da görünüyor:

```bash
# Git cache'i temizle
git rm -r --cached .
git add .
git commit -m "Cache temizlendi"
git push
```

### Yerel dosyanız silindi:

```bash
# Endişelenmeyin, yeniden oluşturabilirsiniz
# Google Drive klasöründeyseniz Drive senkronize edecektir
# Veya Google Sheets'ten yeni kısayol oluşturun
```

### Push authentication hatası:

```bash
# Token ile push yapın
github_duzeltt.bat
```

---

**Not:** `credentials.json` gibi kritik dosyalar güvende, bu sadece ID ve email ifşası.
Yine de best practice gereği kaldırmak daha iyi.
