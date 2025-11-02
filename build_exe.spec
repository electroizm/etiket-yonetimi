# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Proje dizini
project_dir = Path('d:/GoogleDrive/Fiyat/Etiket')

# Veri dosyaları (exe ile birlikte paketlenecek)
# NOT: credentials.json GÜVENLİK nedeniyle DIŞARIDA bırakıldı
# NOT: Etiket.gsheet SPREADSHEET_ID ve email içerdiği için DIŞARIDA bırakıldı
datas = [
    (str(project_dir / 'config.py'), '.'),
    # (str(project_dir / 'credentials.json'), '.'),  # DIŞARIDA TUTULACAK
    (str(project_dir / 'etiketEkle.json'), '.'),
    # (str(project_dir / 'Etiket.gsheet'), '.'),  # DIŞARIDA TUTULACAK (SPREADSHEET_ID içeriyor)
]

# Gizli importlar (PyQt5 ve Google modülleri)
hiddenimports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtPrintSupport',
    'gspread',
    'google.auth',
    'google.oauth2',
    'google_auth_oauthlib',
    'pandas',
    'requests',
    'openpyxl',
    'bs4',
    'reportlab',
    'PIL',
]

a = Analysis(
    [str(project_dir / 'run.py')],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy.testing', 'tkinter'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EtiketYonetimi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # KONSOL PENCERESİNİ GİZLE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # İsterseniz .ico dosyası ekleyebilirsiniz
)
