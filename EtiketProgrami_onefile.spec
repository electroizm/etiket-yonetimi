# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller .spec dosyası - Etiket Programı
--onefile modu: Tek EXE dosyası (portable)
"""

import sys
from pathlib import Path

# Proje dizini
project_dir = Path(r'D:\GoogleDrive\Fiyat\Etiket')

# Veri dosyaları (EXE içine paketlenecek)
datas = [
    (str(project_dir / 'dogtasCom.py'), '.'),  # Web scraper script
    (str(project_dir / 'jsonGoster.py'), '.'),
    (str(project_dir / 'etiketEkle.py'), '.'),
    (str(project_dir / 'etiketYazdir.py'), '.'),
    (str(project_dir / 'config.py'), '.'),
    (str(project_dir / 'etiketEkle.json'), '.'),
    (str(project_dir / 'icon.ico'), '.'),  # Program ikonu (runtime için)
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
    'aiohttp',
    'asyncio',
    'multiprocessing',
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

# --onefile modu: Tek EXE dosyası
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # Binaries EXE içinde
    a.zipfiles,    # Zipfiles EXE içinde
    a.datas,       # Datas EXE içinde
    [],
    name='EtiketProgrami',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Konsol penceresi kapalı
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_dir / 'icon.ico'),  # Program ikonu
)

# NOT: --onefile modunda COLLECT kullanılmaz
