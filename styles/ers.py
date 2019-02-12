import os

from . import Styles

class ERSStyles(Styles):
    def __init__(self):
        super(ERSStyles, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "ers")
        # self._styles = [
        #     {'name' : '?',
        #      'file' : os.path.join(stylePath, 'color_ramps.xml')
        #     },
        # ]
