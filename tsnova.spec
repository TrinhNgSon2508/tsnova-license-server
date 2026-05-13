# tsnova.spec

# =========================================================
# IMPORTS
# =========================================================

from PyInstaller.utils.hooks import (
    collect_submodules
)

# =========================================================
# HIDDEN IMPORTS
# =========================================================

hidden_imports = []

# ---------------------------------------------------------
# PROJECT PACKAGES
# ---------------------------------------------------------

hidden_imports += collect_submodules(
    "pages"
)

hidden_imports += collect_submodules(
    "ui"
)

hidden_imports += collect_submodules(
    "core"
)

hidden_imports += collect_submodules(
    "services"
)

hidden_imports += collect_submodules(
    "utils"
)

# ---------------------------------------------------------
# THIRD PARTY
# ---------------------------------------------------------

hidden_imports += collect_submodules(
    "psutil"
)

hidden_imports += [

    "customtkinter",

    "tkinterdnd2",

    "PIL",

    "PIL.Image",

    "PIL.ImageTk",

    "cv2",

    "numpy"
]

# =========================================================
# ANALYSIS
# =========================================================

a = Analysis(

    ["main.py"],

    pathex=[],

    binaries=[],

    datas=[

    
    ],

    hiddenimports=hidden_imports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    win_no_prefer_redirects=False,

    win_private_assemblies=False,

    cipher=None,

    noarchive=False
)

# =========================================================
# PYZ
# =========================================================

pyz = PYZ(

    a.pure,

    a.zipped_data,

    cipher=None
)

# =========================================================
# EXE
# =========================================================

exe = EXE(

    pyz,

    a.scripts,

    a.binaries,

    a.zipfiles,

    a.datas,

    [],

    name="TSNOVA",

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

    icon=None
)