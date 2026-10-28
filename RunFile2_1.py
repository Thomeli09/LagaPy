import subprocess
from pathlib import Path

exe = Path(
    r"C:\Lagamine\VS_Project\Prepro\x64\Debug\Prepro.exe"
)

RelFolder = Path(r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\dif_mesh.LAG")

process = subprocess.Popen(
    [str(exe)],
    cwd=str(exe.parent),
)

print(f"Process launched with PID: {process.pid}")
