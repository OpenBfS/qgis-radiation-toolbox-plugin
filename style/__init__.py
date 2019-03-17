import os

class StyleError(Exception):
    pass

class Style:
    def __init__(self):
        self._styles = []
        
    def __getitem__(self, index):
        return self._styles[index]

    def __len__(self):
        return len(self._styles)

    def __iter__(self):
        return iter(self._styles)
