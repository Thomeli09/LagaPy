# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib


# Custom Lib
from Python2Lagamine import Lagamine

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
        

    # Metadata
    @property
    def getName(self) -> str:
        if self._Name is None:
            return self.Filepath.stem
        return self._Name

    @getName.setter
    def getName(self, Name: str) -> None:
        self._Name = Name

