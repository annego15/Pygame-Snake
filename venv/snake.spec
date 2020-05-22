# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['snake.py'],
             pathex=['/Users/andresneff/Documents/3. Schule/3. EF/Pygame-Project/venv'],
             binaries=[],
             datas=[('buttons.png', '.'), ('credits.png', '.'), ('game_over.png', '.'), ('PixelGameFont.ttf', '.'), ('tutorial.png', '.'), ('screens.py', '.'), ('game.py', '.'), ('highscore_ai.txt', '.')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='snake',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='snake.app',
             icon=None,
             bundle_identifier=None)
