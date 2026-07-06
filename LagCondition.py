# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib


# Custom Lib


"""
LagCond: Generic class for the initial and boundary conditions of lagamine. 
It is used to read, store and treat the initial and boundary conditions of lagamine in lag and dep files.

# Improvement to be done:
- 
"""
class LagCond():
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
