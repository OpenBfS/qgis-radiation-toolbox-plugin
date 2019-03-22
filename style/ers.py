import os

from . import Style

from qgis.core import QgsStyle

class ERSStyle(Style):
    def __init__(self):
        super(ERSStyle, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "ers")

        self._styleFactory = QgsStyle()
        self._styleFactory.importXml(os.path.join(stylePath, 'color_ramps.xml'))

        for styleName in self._styleFactory.colorRampNames():
            self._styles.append(
                {
                    'name' : styleName,
                    'colorramp' : self._styleFactory.colorRamp(styleName)
                }
            )
