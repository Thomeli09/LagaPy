# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib
import subprocess
from pathlib import Path

# Custom Lib


"""
LagRun: Generic class for running lagamine. 
It is used to read, store and treat the run of lagamine in run files. 

# Improvement to be done:
- Need to launch exe file
- Need to read the output files and check if the run is finished
- Need to select files to run
- Need to check advancement of the run at given refresh time
"""
class LagRun():
    def __init__(self, filepath: str, Name: str | None = None):
        # Metadata
        self._Name = Name
        self._comment = None

        # Input file
        self._workdirectory = None
        self._prepro = None
        self._lagamine = None

        self._lag = None
        self._dat = None

        self._dep = None
        self._lic = None

        self._pri = None

        # Output file
        self._ipn = None
        self._ipe = None


    # Metadata
    @property
    def Name(self) -> str:
        return self._Name

    @Name.setter
    def Name(self, Name: str) -> None:
        self._Name = Name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self._comment = comment

    # Input file
    @property
    def workdirectory(self) -> str:
        return self._workdirectory

    @workdirectory.setter
    def workdirectory(self, workdirectory: str) -> None:
        Path(self.workdirectory).mkdir(parents=True, exist_ok=True)

        path = Path(workdirectory)

        if path.exists() and path.is_dir():
            self._workdirectory = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Work directory not found: {workdirectory}")

    @property
    def prepro(self) -> str:
        return self._prepro

    @prepro.setter
    def prepro(self, prepro: str) -> None:
        path = Path(prepro)
        if path.exists() and path.is_file():
            self._prepro = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Prepro file not found: {prepro}")

    @property
    def lagamine(self) -> str:
        return self._lagamine

    @lagamine.setter
    def lagamine(self, lagamine: str) -> None:
        path = Path(lagamine)
        if path.exists() and path.is_file():
            self._lagamine = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Lagamine file not found: {lagamine}")

    @property
    def lag(self) -> str:
        return self._lag

    @lag.setter
    def lag(self, lag: str) -> None:
        path = Path(lag)
        if path.exists() and path.is_file():
            self._lag = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Lag file not found: {lag}")

    @property
    def dat(self) -> str:
        return self._dat

    @dat.setter
    def dat(self, dat: str) -> None:
        path = Path(dat)
        if path.exists() and path.is_file():
            self._dat = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Dat file not found: {dat}")

    @property
    def dep(self) -> str:
        return self._dep

    @dep.setter
    def dep(self, dep: str) -> None:
        path = Path(dep)
        if path.exists() and path.is_file():
            self._dep = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Dep file not found: {dep}")

    @property
    def lic(self) -> str:
        return self._lic

    @lic.setter
    def lic(self, lic: str) -> None:
        path = Path(lic)
        if path.exists() and path.is_file():
            self._lic = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Lic file not found: {lic}")

    @property
    def pri(self) -> str:
        return self._pri

    @pri.setter
    def pri(self, pri: str) -> None:
        path = Path(pri)
        if path.exists() and path.is_file():
            self._pri = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Pri file not found: {pri}")

    # Output file
    @property
    def ipn(self) -> str:
        return self._ipn

    @ipn.setter
    def ipn(self, ipn: str) -> None:
        path = Path(ipn)
        if path.exists() and path.is_file():
            self._ipn = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Ipn file not found: {ipn}")

    @property
    def ipe(self) -> str:
        return self._ipe

    @ipe.setter
    def ipe(self, ipe: str) -> None:
        path = Path(ipe)
        if path.exists() and path.is_file():
            self._ipe = path.resolve().as_posix()
        else:
            raise FileNotFoundError(f"Ipe file not found: {ipe}")

    # Command to run
    def processing(self) -> None:
        """
        Process the input file before running the lagamine executable. This method runs the Prepro.exe with the specified arguments.
        """
        # Verifies that all the needed files are present before running the executable
        if not all([self.prepro is not None, self.lag is not None]):
            raise FileNotFoundError("One or more required files are missing.")

        if self.workdirectory is not None:
            # Change the current working directory to the specified work directory
            try:
                subprocess.run(["cd", self.workdirectory], shell=True, check=True)
            except Exception as e:
                print(f"An error occurred while changing the working directory: {e}")
                return

        try:
            subprocess.run(
                [
                    self.prepro,
                    self.lag,
                    r"x",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the executable: {e}")

    def run(self) -> None:
        """
        Run the lagamine executable with the specified input file.
        """
        # Verifies that all the needed files are present before running the executable
        if not all([self.lagamine is not None, self.dat is not None, self.lag is not None]):
            raise FileNotFoundError("One or more required files are missing.")

        if self.workdirectory is not None:
            # Change the current working directory to the specified work directory
            try:
                subprocess.run(["cd", self.workdirectory], shell=True, check=True)
            except Exception as e:
                print(f"An error occurred while changing the working directory: {e}")
                return

        try:
            subprocess.run(
                [
                    self.lagamine,
                    self.dat,
                    self.lag,
                    r"x",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the executable: {e}")

    def generatebat(self, output_path: str, prepro: bool = True, lagamine: bool = True) -> None:
        """
        Generate a .bat file to run the lagamine executable with the specified input file.
        """
        # Verifies that all the needed files are present before generating the .bat file
        if not all([self.lagamine is not None, self.dat is not None, self.lag is not None]):
            raise FileNotFoundError("One or more required files are missing.")

        bat_content = "@echo off\n"
        if self.workdirectory is not None:
            bat_content += f'cd "{self.workdirectory}"\n'

        if prepro:
            bat_content += f'"{self.prepro}" "{self.lag}" x\n'
            
        if lagamine:
            bat_content += f'"{self.lagamine}" "{self.dat}" "{self.lag}" x\n'
        
        with open(output_path, 'w') as bat_file:
            bat_file.write(bat_content)



