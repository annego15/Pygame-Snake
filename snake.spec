# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['snake.py'],
             pathex=['/Users/andresneff/Documents/3. Schule/3. EF/Pygame-Project'],
             binaries=[],
             datas=[('buttons.png', '.'), ('credits.png', '.'), ('game_over.png', '.'), ('PixelGameFont.ttf', '.'), ('tutorial.png', '.'), ('highscore_ai.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='snake',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='snake')
