@echo off
REM =================================================================
REM  Etiket.gsheet Dosyasını GitHub'dan Kaldırma Scripti
REM =================================================================

echo.
echo ========================================
echo   Etiket.gsheet GitHub'dan Kaldirilacak
echo ========================================
echo.

cd /d "d:\GoogleDrive\Fiyat\Etiket"

REM Mevcut durumu göster
echo [1/4] Mevcut durum kontrol ediliyor...
git status --short
echo.

REM Git'ten kaldır (yerel dosya kalacak)
echo [2/4] Etiket.gsheet git'ten kaldiriliyor...
echo.
echo     NOT: Dosya sadece git'ten silinecek, bilgisayarinizda kalacak!
echo.

git rm --cached Etiket.gsheet 2>nul

if errorlevel 1 (
    echo     [INFO] Dosya zaten git'te yok veya kaldirilmis
) else (
    echo     [OK] Dosya git'ten kaldirildi
)
echo.

REM .gitignore'un güncellendiğini göster
echo [3/4] .gitignore kontrol ediliyor...
findstr /C:"Etiket.gsheet" .gitignore >nul

if errorlevel 1 (
    echo     [UYARI] Etiket.gsheet .gitignore'da yok!
    echo     Manuel olarak ekleyin!
) else (
    echo     [OK] Etiket.gsheet .gitignore'da mevcut
)
echo.

REM Commit oluştur
echo [4/4] Commit olusturuluyor...
echo.

git add .gitignore
git commit -m "Guvenlik: Etiket.gsheet dosyasi kaldirildi

- Etiket.gsheet SPREADSHEET_ID ve email bilgisi iceriyordu
- .gitignore'a *.gsheet ve Etiket.gsheet eklendi
- Yerel dosya korundu, sadece git'ten kaldirildi"

if errorlevel 1 (
    echo     [INFO] Commit basarisiz veya degisiklik yok
    echo.
) else (
    echo     [OK] Commit basarili
    echo.
)

REM Durum göster
echo.
echo ========================================
echo   Hazir!
echo ========================================
echo.
echo Simdi GitHub'a yuklemeniz gerekiyor:
echo.
echo   git push
echo.
echo Veya token ile:
echo   git push origin main
echo.
echo SONUC:
echo   [OK] Etiket.gsheet GitHub'dan kaldirilacak
echo   [OK] Yerel dosyaniz duruyor (silinmedi)
echo   [OK] Gelecekte otomatik ignore edilecek
echo.

choice /C YN /M "Simdi GitHub'a yuklensin mi"

if errorlevel 2 (
    echo.
    echo [INFO] Yukleme iptal edildi
    echo Manuel olarak yuklemek icin: git push
    echo.
) else (
    echo.
    echo [PUSH] GitHub'a yukleniyor...
    echo.

    git push

    if errorlevel 1 (
        echo     [HATA] Push basarisiz!
        echo.
        echo     Token gerekiyorsa:
        echo       github_duzeltt.bat scriptini calistirin
        echo.
    ) else (
        echo     [OK] GitHub'a yukleme basarili!
        echo.
        echo ========================================
        echo   BASARILI!
        echo ========================================
        echo.
        echo Etiket.gsheet artik GitHub'da gorulmeyecek!
        echo.
    )
)

pause
