import subprocess


if __name__ == "__main__":
    # Run the Prepro.exe and Lagamine.exe with the specified arguments
    subprocess.run(
        [
            r"C:\Users\Thommes Eliott\Downloads\LagamineTest\Prepro.exe",
            r"C:\Users\Thommes Eliott\Downloads\LagamineTest\HYPOFE2_REACT.LAG",
            r"x",
        ],
        check=True,
    )

    subprocess.run(
        [
            r"C:\Users\Thommes Eliott\Downloads\LagamineTest\Lagamine.exe",
            r"C:\Users\Thommes Eliott\Downloads\LagamineTest\HYPOFE2_REACT_DAT.DAT",
            r"C:\Users\Thommes Eliott\Downloads\LagamineTest\HYPOFE2_REACT.LAG",
            r"x",
        ],
        check=True,
    )

# Il est important que le code soit capable de gérer le cas de blocage de code, vérifie que les fichiers existent avant de lancer l'excécutable
#, et gère les exceptions pour éviter que le programme ne plante en cas d'erreur.