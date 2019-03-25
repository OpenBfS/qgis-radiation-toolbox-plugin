import os

from . import Style

class PEIStyle(Style):
    def __init__(self):
        super(PEIStyle, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "pei")
        self._styles = [
            {'name' : 'simple',
             'file' : os.path.join(stylePath, 'MobDose_simple_style.qml')
            }
        ]
