@echo off
chcp 65001 >nul
echo ===============================================
echo   Doğtaş Web Scraper Build (--onefile)
echo ===============================================
echo.

REM 1. Dizin kontrolü
cd /d D:\GoogleDrive\Fiyat\Etiket
if %errorlevel% neq 0 (
    echo [HATA] Dizin bulunamadı!
    pause
    exit /b 1
)

echo [1/3] Spec dosyası kontrol ediliyor...
if exist "dogtasCom.spec" (
    echo     [OK] dogtasCom.spec bulundu
) else (
    echo     [HATA] dogtasCom.spec bulunamadı!
    pause
    exit /b 1
)

echo.
echo [2/3] PyInstaller build başlatılıyor...
echo     Mode: --onefile (tek EXE)
echo.

C:\Python\python.exe -m PyInstaller dogtasCom.spec --clean

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Build başarısız!
    pause
    exit /b 1
)

echo.
echo [3/3] Build doğrulanıyor...
if exist "dist\dogtasCom.exe" (
    echo     [OK] dogtasCom.exe oluşturuldu
    for %%I in ("dist\dogtasCom.exe") do echo     Boyut: %%~zI bytes
) else (
    echo     [HATA] dogtasCom.exe oluşturulamadı!
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Build Başarılı!
echo ===============================================
echo   Dosya: dist\dogtasCom.exe
echo ===============================================
echo.

pause
