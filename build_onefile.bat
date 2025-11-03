@echo off
REM =================================================================
REM  Etiket Programı - Tek Dosya (--onefile) Build Script
REM =================================================================

echo.
echo ========================================
echo   Etiket Programi - Build Baslatiyor
echo   Mod: TEK DOSYA (--onefile)
echo ========================================
echo.

cd /d "D:\GoogleDrive\Fiyat\Etiket"

REM Icon dosyasini kontrol et
echo [1/4] Icon dosyasi kontrol ediliyor...
if exist "icon.ico" (
    echo     [OK] icon.ico bulundu
    dir icon.ico | findstr /C:"icon.ico"
) else (
    echo     [HATA] icon.ico bulunamadi!
    pause
    exit /b 1
)
echo.

REM Eski build dosyalarını temizle
echo [2/6] Eski build dosyalari temizleniyor...
if exist "build" rmdir /s /q "build"
if exist "dist\EtiketProgrami.exe" del /f /q "dist\EtiketProgrami.exe"
if exist "dist\dogtasCom.exe" del /f /q "dist\dogtasCom.exe"
echo     [OK] Temizlik tamamlandi
echo.

REM dogtasCom.exe build et (önce)
echo [3/6] dogtasCom.exe build ediliyor...
echo     Web scraper icin ayri EXE (Python dependency yok)
echo.
C:\Python\python.exe -m PyInstaller dogtasCom.spec --clean
if errorlevel 1 (
    echo.
    echo     [HATA] dogtasCom.exe build basarisiz!
    pause
    exit /b 1
)
echo     [OK] dogtasCom.exe olusturuldu
echo.

REM PyInstaller ile build (--onefile)
echo [4/6] PyInstaller calistiriliyor (ana program)...
echo     Spec dosyasi: EtiketProgrami_onefile.spec
echo     Mod: --onefile (tek dosya modu)
echo     Uyari: Build suresi uzun olabilir (1-3 dakika)
echo.

C:\Python\python.exe -m PyInstaller EtiketProgrami_onefile.spec --clean

if errorlevel 1 (
    echo.
    echo     [HATA] Build basarisiz!
    echo.
    pause
    exit /b 1
)

echo.
echo     [OK] Build tamamlandi
echo.

REM dogtasCom.exe'yi ana EXE'nin yanina kopyala
echo [5/6] dogtasCom.exe kopyalaniyor...
if exist "dist\dogtasCom.exe" (
    REM Zaten dist/ altında olmalı, kontrol et
    echo     [OK] dogtasCom.exe dist/ klasorunde mevcut
) else (
    echo     [HATA] dogtasCom.exe bulunamadi!
)
echo.

REM Sonuçları göster
echo [6/6] Build sonuclari:
echo.

if exist "dist\EtiketProgrami.exe" (
    echo     [OK] EXE DOSYALARI olusturuldu:
    echo          1. dist\EtiketProgrami.exe (ana program)
    echo          2. dist\dogtasCom.exe (web scraper)
    echo.

    REM Dosya boyutlarını göster
    echo     [INFO] Dosya boyutlari:
    dir "dist\EtiketProgrami.exe" | findstr /C:"EtiketProgrami.exe"
    dir "dist\dogtasCom.exe" | findstr /C:"dogtasCom.exe"
    echo.

    REM Icon kontrolu
    echo     [INFO] Icon kontrol ediliyor...
    C:\Python\python.exe -c "import sys; from PyQt5.QtWidgets import QApplication; from PyQt5.QtGui import QIcon; app = QApplication(sys.argv); icon = QIcon('dist/EtiketProgrami.exe'); sizes = [s.width() for s in icon.availableSizes()]; print('      Icon boyutlari:', sizes if sizes else 'YOK (HATA!)')" 2>nul
    echo.

    echo ========================================
    echo   BUILD BASARILI!
    echo ========================================
    echo.
    echo Programi calistirmak icin:
    echo   dist\EtiketProgrami.exe
    echo.
    echo.
    echo ===== TEK DOSYA MODU AVANTAJLARI =====
    echo   + Tek EXE dosyasi (portable)
    echo   + Kolay dagitim (sadece 1 dosya)
    echo   + Temiz gorunum (klasor karisikligi yok)
    echo.
    echo ===== ONEMLI NOTLAR =====
    echo   1. EXE ilk calistirmada YAVAS baslayabilir
    echo      (Gecici klasore dosyalari acar: ~5-10 saniye)
    echo.
    echo   2. etiketEkle.json gibi yazilabilir dosyalar
    echo      EXE'nin YANINDA olusturulacak
    echo.
    echo   3. credentials.json ve token.pickle dosyalarini
    echo      EXE'nin yanina koymayi UNUTMAYIN!
    echo.
    echo   4. dogtasCom.exe web taramasi icin
    echo      otomatik olarak calistirilir
    echo      (Python kurulumuna GEREK YOK)
    echo.
    echo ===== ICON KONTROL =====
    echo   - Dosya Gezgini: Icon gorunmeli
    echo   - Gorev cubugu: Icon gorunmeli
    echo   - Icon gorunmuyorsa: Bilgisayari yeniden baslatin
    echo.
) else (
    echo     [HATA] EXE olusturulamadi!
    echo     Lutfen hata mesajlarini kontrol edin
    echo.
)

pause
