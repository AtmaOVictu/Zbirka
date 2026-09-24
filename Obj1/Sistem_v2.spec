# -*- mode: python ; coding: utf-8 -*-
# SISTEM ∅→∆→∂→∮ v2.0 - PyInstaller Spec File
# Avtor: Luka + Vibe
# Datum: 19. 9. 2026
#
# Namestitev PyInstaller:
#   pip install pyinstaller
#
# Zagon:
#   pyinstaller Sistem_v2.spec
#   or: python -m PyInstaller Sistem_v2.spec
#
# Izhod: dist/Sistem_v2.exe

block_cipher = None

a = Analysis(
    ['sistem_gui_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database.json', '.'),
        ('sistem.db', '.'),
        ('icon.ico', '.'),
        ('*.md', '.'),
    ],
    hiddenimports=[
        'PySide6.QtWidgets',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtPrintSupport',
        'PySide6.QtSvg',
        'encodings.*',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,
)

# Windowed application (no console)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

ex = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sistem_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version='2.0.0',
    company_name='RozetniKamni',
    product_name='SISTEM ∅→∆→∂→∮ v2.0',
    copyright='© 2026 Luka + Vibe',
    trademark=None,
    info_plist={
        'CFBundleName': 'SISTEM',
        'CFBundleDisplayName': 'SISTEM ∅→∆→∂→∮',
        'CFBundleIdentifier': 'com.rozetnikamni.sistem',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0',
        'NSHumanReadableCopyright': '© 2026 Luka + Vibe',
    },
)

# Build configuration
coll = COLLECT(
    ex,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Sistem_v2',
)
