from qgis.core import QgsFeature, QgsPointXY, QgsGeometry

from . import LayerBase, LayerType

class PEILayer(LayerBase):
    def __init__(self, fileName, storageFormat):
        """ERS memory-based read-only layer.

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
        """
        super(PEILayer, self).__init__(fileName, storageFormat)

        # layer type
        self.layerType = LayerType.PEI

    def _item2feat(self, item):
        """Create QgsFeature from data item.
        """
        feat = QgsFeature()

        # set geometry
        point = QgsPointXY(float(item['Lat']), float(item['Lon']))
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # set attributes
        # feat.setAttributes(list(item.values()))

        return feat
