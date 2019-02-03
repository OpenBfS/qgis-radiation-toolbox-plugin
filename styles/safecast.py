import os

from . import Styles

class SafecastStyles(Styles):
    def __init__(self):
        super(SafecastStyles, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "safecast")
        self._styles = [
            {'name' : '0.08 - 10.00 microSv/h',
             'file' : os.path.join(stylePath, 'normal.qml')
            },
            {'name' : '0.05 - 200.00 microSv/h',
             'file' : os.path.join(stylePath, 'high.qml')
            }
        ]
