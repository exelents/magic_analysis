# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages', 'C:\\pystuff\\magic_analysis'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['statsmodels'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/statsmodels", prefix="statsmodels")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/numpy", prefix="numpy")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/pandas", prefix="pandas")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/scipy", prefix="scipy")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/pyfiglet", prefix="pyfiglet")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/patsy", prefix="patsy")
a.datas += Tree("C:/Users/user/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/dateutil", prefix="dateutil")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='rose-48.ico')
