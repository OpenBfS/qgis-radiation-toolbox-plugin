from qgis.core import QgsFeature, QgsPointXY, QgsGeometry
 
from . import LayerBase

class ERSLayer(LayerBase):
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
