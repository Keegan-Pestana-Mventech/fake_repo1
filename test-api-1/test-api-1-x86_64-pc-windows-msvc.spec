# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = [('C:\\Users\\KeeganPestana\\Documents\\Mventech\\Multi_Sidecar_Bundler\\fake_repo1\\test-api-1\\src', 'src')]
binaries = []
hiddenimports = ['numpy', 'numpy_financial', 'fastapi', 'uvicorn', 'pydantic', 'pydantic_core', 'starlette', 'numpy.core', 'numpy.core._multiarray_umath', 'win32timezone']
datas += collect_data_files('numpy')
datas += collect_data_files('numpy_financial')
datas += collect_data_files('fastapi')
datas += collect_data_files('uvicorn')
datas += collect_data_files('pydantic')
datas += collect_data_files('pydantic_core')
datas += collect_data_files('starlette')
datas += copy_metadata('numpy')
datas += copy_metadata('numpy_financial')
binaries += collect_dynamic_libs('numpy')
binaries += collect_dynamic_libs('numpy_financial')
binaries += collect_dynamic_libs('fastapi')
binaries += collect_dynamic_libs('uvicorn')
binaries += collect_dynamic_libs('pydantic')
binaries += collect_dynamic_libs('pydantic_core')
binaries += collect_dynamic_libs('starlette')
binaries += collect_dynamic_libs('numpy.core')
hiddenimports += collect_submodules('numpy')
hiddenimports += collect_submodules('numpy_financial')
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('pydantic_core')
hiddenimports += collect_submodules('starlette')
tmp_ret = collect_all('numpy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('numpy_financial')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\KeeganPestana\\Documents\\Mventech\\Multi_Sidecar_Bundler\\fake_repo1\\test-api-1\\src\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'tk', '_tkinter', 'PyQt5', 'PyQt6', 'wx', 'matplotlib'],
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
    name='test-api-1-x86_64-pc-windows-msvc',
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
)
