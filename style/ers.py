import os

from . import Style

class ERSStyle(Style):
    def __init__(self):
        super(ERSStyle, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "ers")

        # static styles
        self._styles = [
            {'name' : 'simple',
             'file' : os.path.join(stylePath, 'ERS_simple_style.qml')
            }
        ]

        # dynamic styles
        self._load_color_ramps(
            os.path.join(stylePath, 'color_ramps.xml'),
            attribute='DHSR'
        )
