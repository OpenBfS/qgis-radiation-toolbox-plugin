import os

from . import Style

from qgis.core import QgsStyle

class ERSStyle(Style):
    def __init__(self):
        super(ERSStyle, self).__init__()

        stylePath = os.path.join(os.path.dirname(__file__), "ers")

        styleFactory = QgsStyle()
        styleFactory.importXml(os.path.join(stylePath, 'color_ramps.xml'))

        for styleName in styleFactory.colorRampNames():
            self._styles.append(
                {'name' : styleName}
            )
