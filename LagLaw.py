# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library 


# Other Lib


# Custom Lib


"""
LagLaw: Generic class for the law of lagamine. 
It is used to read, store and treat the law of lagamine.

# Improvement to be done:
- 
"""
class LagLaw():
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
