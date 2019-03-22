import os
import sys

from qgis.core import QgsFeature, QgsPointXY, QgsGeometry, QgsGraduatedSymbolRenderer
 
from . import LayerBase, LayerType
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from style.ers import ERSStyle

class ERSLayer(LayerBase):
    def __init__(self, fileName, storageFormat):
        """ERS memory-based read-only layer.

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
        """
        super(ERSLayer, self).__init__(fileName, storageFormat)

        # layer type
        self.layerType = LayerType.ERS

        # style
        self._style = ERSStyle()
        self._renderer = None

    def _item2feat(self, item):
        """Create QgsFeature from data item.
        """
        feat = QgsFeature()

        # set geometry
        # PN ... Measurement or sample point coordinate N-S (latitude) Numeric
        # PE ... Measurement or sample point coordinate E-W (longitude) Numeric
        point = QgsPointXY(float(item['PE']), float(item['PN']))
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # set attributes
        feat.setAttributes(list(item.values()))

        return feat

    def setStyle(self, idx):
        """Set layer style.

        :param int idx: style (combobox) index
        """
        numberOfClasses = 6

        if not self._renderer:
            self._renderer = QgsGraduatedSymbolRenderer()
            self._renderer.setClassAttribute("DHSR")
            self._renderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
            self._renderer.updateClasses(
                self, QgsGraduatedSymbolRenderer.EqualInterval, numberOfClasses
            )
            self.setRenderer(self._renderer)

        self._renderer.updateColorRamp(self._style[idx]['colorramp'])
