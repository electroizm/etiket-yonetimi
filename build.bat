@echo off
REM =================================================================
REM  Etiket Yönetimi - EXE Build Script
REM =================================================================

echo.
echo ========================================
echo   Etiket Yonetimi - EXE Olusturuluyor
echo ========================================
echo.

REM PyInstaller kurulu mu kontrol et
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [HATA] PyInstaller yuklu degil!
    echo.
    echo PyInstaller yukleniyor...
    pip install pyinstaller
    echo.
)

REM Eski build dosyalarını temizle
echo [1/4] Eski build dosyalari temizleniyor...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo     - Temizleme tamamlandi
echo.

REM EXE oluştur
echo [2/4] EXE olusturuluyor...
pyinstaller --clean build_exe.spec
echo.

REM Sonucu kontrol et
if exist "dist\EtiketYonetimi.exe" (
    echo [3/4] EXE basariyla olusturuldu!
    echo.

    REM Dagitim kilavuzunu kopyala
    if exist "DAGITIM_KILAVUZU.md" (
        copy /Y "DAGITIM_KILAVUZU.md" "dist\" >nul
        echo     - Dagitim kilavuzu kopyalandi
    )

    REM credentials.json template olustur (gercek dosya dahil EDILMEDI!)
    echo. > "dist\credentials.json.BURAYA_KOYUN.txt"
    echo ONEMLI: credentials.json dosyasini bu klasore koyun! >> "dist\credentials.json.BURAYA_KOYUN.txt"
    echo. >> "dist\credentials.json.BURAYA_KOYUN.txt"
    echo Program calisirken credentials.json dosyasini burada arayacak. >> "dist\credentials.json.BURAYA_KOYUN.txt"
    echo. >> "dist\credentials.json.BURAYA_KOYUN.txt"
    echo Detayli talimatlar icin DAGITIM_KILAVUZU.md dosyasina bakiniz. >> "dist\credentials.json.BURAYA_KOYUN.txt"
    echo.
    echo     - Credentials hatirlatici dosyasi olusturuldu

    REM Dosya boyutunu göster
    echo [4/4] Dosya bilgileri:
    dir "dist\EtiketYonetimi.exe" | findstr "EtiketYonetimi.exe"
    echo.

    echo ========================================
    echo   BASARILI!
    echo ========================================
    echo.
    echo EXE dosyasi: dist\EtiketYonetimi.exe
    echo.
    echo NOT: Programi baska bir bilgisayarda calistirmak icin
    echo      dist\ klasorundeki TUM dosyalari kopyalayin!
    echo.
) else (
    echo [HATA] EXE olusturulamadi!
    echo Lutfen hata mesajlarini kontrol edin.
    echo.
)

pause
