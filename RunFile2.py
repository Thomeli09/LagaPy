import subprocess


if __name__ == "__main__":
    # Run the Prepro.exe and Lagamine.exe with the specified arguments

    subprocess.run(
        [
            r"C:\Lagamine\VS_Project\Prepro\x64\Debug\Prepro.exe",
            r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\dif_mesh.LAG",
        ],
        check=True,
    )

    subprocess.run(
        [
            r"C:\Lagamine\VS_Project\Lagamine\x64\Debug\Lagamine.exe",
            r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\loading_1.DAT",
            r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\dif_mesh.LAG",
        ],
        check=True,
    )
