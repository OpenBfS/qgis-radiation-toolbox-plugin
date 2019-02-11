from qgis.core import QgsFeature, QgsPointXY, QgsGeometry
 
from . import LayerBase, LayerType

class ERSLayer(LayerBase):
    def __init__(self, fileName, storageFormat):
        """ERS memory-based read-only layer.

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
        """
        super(ERSLayer, self).__init__(fileName, storageFormat)

        # layer type
        self.layerType = LayerType.ERS

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
        # print ('y', len(list(item.values())))
        feat.setAttributes(list(item.values()))

        return feat
