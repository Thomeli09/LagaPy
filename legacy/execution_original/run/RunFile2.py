import subprocess


if __name__ == "__main__":
    # Run the Prepro.exe and Lagamine.exe with the specified arguments
    subprocess.run(
        [
            r"C:\LagaProgs\Prepro.exe",
            r"C:\Simulations\example.LAG",
            r"x",
        ],
        check=True,
    )

    subprocess.run(
        [
            r"C:\LagaProgs\Lagamine.exe",
            r"C:\Simulations\example.DAT",
            r"C:\Simulations\example.LAG",
            r"x",
        ],
        check=True,
    )

# Il est important que le code soit capable de gérer le cas de blocage de code, vérifie que les fichiers existent avant de lancer l'excécutable
#, et gère les exceptions pour éviter que le programme ne plante en cas d'erreur.