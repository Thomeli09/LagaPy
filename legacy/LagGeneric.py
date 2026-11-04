# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib


# Custom Lib


"""
LagGeneric: Generic class for the lagamine management. It is used to define the generic properties of lagamine management. 
It is used to store data from different sources and to treat them.

# Improvement to be done:
- 
"""
class LagGeneric():
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

