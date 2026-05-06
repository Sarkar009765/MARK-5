# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('.env', '.'),
        ('templates', 'templates'),
    ],
    hiddenimports=[
        'brain', 'brain.llm', 'brain.prompts',
        'voice', 'voice.tts', 'voice.stt', 'voice.wakeword',
        'tools', 'tools.base', 'tools.system', 'tools.browser', 'tools.files', 'tools.web',
        'memory', 'memory.db',
        'pyttsx3', 'pyttsx3.drivers', 'pyttsx3.drivers.sapi5',
        'tinydb', 'google.generativeai',
        'psutil', 'pyautogui', 'pyperclip',
        'telegram', 'telegram.ext',
        'flask', 'werkzeug', 'jinja2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ClawVis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
