# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib


# Custom Lib


"""
LagPri: Generic class for the data printing of lagamine. 
It is used to read, store and treat the data pri files in lagamine.

# Improvement to be done:
- 
"""
class LagPri():
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
