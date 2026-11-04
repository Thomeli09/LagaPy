# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library for management of lagamine data and its treatment. It is used to store data from different sources and to treat them.


# Other Lib


# Custom Lib


"""
Lagamine: Generic class for the management of data from different sources. 
It is used to store data and to treat them.

# Improvement to be done:
- 
"""
class Lagamine():
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
