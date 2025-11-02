@echo off
REM =================================================================
REM  GitHub Yükleme Scripti - Etiket Yönetimi
REM =================================================================

echo.
echo ========================================
echo   GitHub'a Yukleme Hazirlaniyor
echo ========================================
echo.

REM Hassas dosyaları kontrol et
echo [1/5] Guvenlik kontrolu yapiliyor...
echo.

if exist "credentials.json" (
    echo     [OK] credentials.json mevcut ^(ama yuklenmeyecek^)
) else (
    echo     [INFO] credentials.json yok ^(normal^)
)

if exist "token.pickle" (
    echo     [OK] token.pickle mevcut ^(ama yuklenmeyecek^)
) else (
    echo     [INFO] token.pickle yok ^(normal^)
)

if exist "etiketEkle.json" (
    echo     [OK] etiketEkle.json mevcut ^(ama yuklenmeyecek^)
) else (
    echo     [INFO] etiketEkle.json yok
)

echo.
echo     .gitignore hassas dosyalari koruyacak!
echo.

REM Git kurulu mu kontrol et
echo [2/5] Git kontrolu yapiliyor...
git --version >nul 2>&1
if errorlevel 1 (
    echo     [HATA] Git yuklu degil!
    echo     Git yuklemek icin: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo     [OK] Git mevcut
echo.

REM Git repo var mı kontrol et
if not exist ".git" (
    echo [3/5] Git repository baslatiliyor...
    git init
    echo     [OK] Git repository olusturuldu
    echo.

    echo     ONEMLI: GitHub'da repository olusturup URL'yi girin:
    echo     Ornek: https://github.com/KULLANICI_ADI/etiket-yonetimi.git
    echo.
    set /p REPO_URL="Repository URL: "

    if defined REPO_URL (
        git remote add origin !REPO_URL!
        echo     [OK] Remote repository eklendi
    ) else (
        echo     [UYARI] Repository URL girilmedi, manuel olarak ekleyin:
        echo     git remote add origin URL
    )
    echo.
) else (
    echo [3/5] Git repository mevcut
    echo.
)

REM Dosyaları stage'e al
echo [4/5] Dosyalar ekleniyor...
git add .
echo     [OK] Dosyalar eklendi
echo.

echo     Yuklenen dosyalar:
git status --short
echo.

REM Commit oluştur
echo [5/5] Commit olusturuluyor...
echo.
echo     Commit mesaji girin ^(bos birakirsaniz varsayilan kullanilir^):
set /p COMMIT_MSG="Mesaj: "

if not defined COMMIT_MSG (
    set COMMIT_MSG=Etiket Yonetimi Sistemi - Ilk Commit
)

git commit -m "%COMMIT_MSG%"

if errorlevel 1 (
    echo     [UYARI] Commit basarisiz veya degisiklik yok
    echo.
) else (
    echo     [OK] Commit basarili
    echo.
)

REM Push teklif et
echo.
echo ========================================
echo   Hazir!
echo ========================================
echo.
echo Simdi GitHub'a yuklemek ister misiniz? ^(git push^)
echo.
echo NOT: Ilk kez yukluyorsaniz su komutu kullanin:
echo   git push -u origin main
echo.
echo Sonraki yukleme icin:
echo   git push
echo.

choice /C YN /M "Simdi yuklensin mi"

if errorlevel 2 (
    echo.
    echo [INFO] Yukleme iptal edildi
    echo Manuel olarak yuklemek icin:
    echo   git push -u origin main
    echo.
) else (
    echo.
    echo [PUSH] GitHub'a yukleniyor...
    echo.

    git push -u origin main 2>nul

    if errorlevel 1 (
        echo     [HATA] Push basarisiz!
        echo.
        echo     Olasi sebepler:
        echo     1. Remote repository ayarlanmamis
        echo     2. Branch adi farkli ^(master vs main^)
        echo     3. Kimlik dogrulama hatasi
        echo.
        echo     Manuel push icin:
        echo       git push -u origin main
        echo       veya
        echo       git push -u origin master
        echo.
    ) else (
        echo     [OK] GitHub'a yukleme basarili!
        echo.
        echo ========================================
        echo   BASARILI!
        echo ========================================
        echo.
        echo GitHub repository URL:
        git remote get-url origin
        echo.
    )
)

echo.
echo Guvenlik Kontrol:
echo -----------------
echo credentials.json yuklenmedi: TAMAM
echo token.pickle yuklenmedi: TAMAM
echo etiketEkle.json yuklenmedi: TAMAM
echo.

pause
