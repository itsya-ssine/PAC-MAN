# PyInstaller spec: build with `make package` -> dist/pacman/
# The MLX shared library is bundled by PyInstaller's hooks when the
# `mlx` module is installed; check the result on a clean machine.
a = Analysis(
    ['pac-man.py'],
    pathex=['.'],
    binaries=[],
    datas=[('config.json', '.'), ('README_GAME.txt', '.')],
    hiddenimports=['mlx', 'mazegen'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pacman',
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name='pacman',
)
