# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller .spec dosyası - Doğtaş Web Scraper
--onefile modu: Tek EXE dosyası (subprocess için)
"""

import sys
from pathlib import Path

project_dir = Path(r'D:\GoogleDrive\Fiyat\Etiket')

# Data dosyaları (runtime'da gerekli)
datas = [
    (str(project_dir / 'config.py'), '.'),
]

# Gizli importlar
hiddenimports = [
    'aiohttp',
    'asyncio',
    'bs4',
    'BeautifulSoup',
    'pandas',
    'requests',
    'openpyxl',
    'gspread',
    'google.auth',
    'google.oauth2',
    'google.oauth2.service_account',
    'google.oauth2.credentials',
    'google.auth.transport.requests',
    'google_auth_oauthlib',
    'google_auth_oauthlib.flow',
    'pickle',
    'logging',
    'xml.etree.ElementTree',
    'json',
    're',
    'time',
    'datetime',
    'urllib.parse',
    'typing',
    'pathlib',
    'io',
]

a = Analysis(
    [str(project_dir / 'dogtasCom.py')],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy.testing', 'tkinter', 'PyQt5'],
    noarchive=False,
)

pyz = PYZ(a.pure)

# --onefile: Tek EXE (subprocess için)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='dogtasCom',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Konsol penceresi yok
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
