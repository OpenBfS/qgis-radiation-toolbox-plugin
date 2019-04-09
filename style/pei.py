import os

from . import Style

class PEIStyle(Style):
    def __init__(self):
        super(PEIStyle, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "pei")

        # static styles
        self._styles = [
            {'name' : 'MobDose simple',
             'file' : os.path.join(stylePath, 'MobDose_simple_style.qml')
            },
            {'name' : 'IRIS simple',
             'file' : os.path.join(stylePath, 'IRIS_simple_style.qml')
            }
        ]

        # dynamic styles
        self._load_color_ramps(
            os.path.join(stylePath, 'color_ramps.xml'),
            attribute='DosG'
        )
