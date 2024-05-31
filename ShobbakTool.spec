# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/shobbak prject/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('D:/shobbak prject/assets/logo.png', 'assets'),
        ('D:/shobbak prject/assets/icon.png', 'assets')
    ],
    hiddenimports=[
        'skimage',
        'transformers.pipelines',
        'transformers.dynamic_module_utils',
        'transformers.image_utils',
        'transformers.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'rembg',    
    ],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=True,
    name='ShobbakTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\ziadw\\OneDrive\\Desktop\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ShobbakTool',
)