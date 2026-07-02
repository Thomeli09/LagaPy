# -*- coding: utf-8 -*-
"""
Created on 02-07-2026

@author: Thommes Eliott
"""

# Library for data storage and treatment 


# Other Lib


# Custom Lib


"""
Storage: Generic class for data storage and treatment. It is used to store data from different sources and to treat them.

# Improvement to be done:
- 
"""
class Storage(ABC):
    def __init__(self, filepath: str | Path,
        name: str | None = None,
    ):
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
