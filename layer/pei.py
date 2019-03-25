from qgis.core import QgsFeature, QgsPointXY, QgsGeometry

from . import LayerBase, LayerType
from style.pei import PEIStyle

class PEILayer(LayerBase):
    def __init__(self, fileName, storageFormat):
        """ERS memory-based read-only layer.

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
        """
        super(PEILayer, self).__init__(fileName, storageFormat)

        # layer type
        self.layerType = LayerType.PEI

        # style
        self._style = PEIStyle()

    def _item2feat(self, item):
        """Create QgsFeature from data item.
        """
        feat = QgsFeature()

        # set geometry
        point = QgsPointXY(float(item['Lon']), float(item['Lat']))
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # set attributes
        feat.setAttributes(list(item.values()))

        return feat


    def _setShownFields(self, fields):
        """Set shown fields.

        :param list fields: list of fields
        """
        config = self.attributeTableConfig()
        columns = config.columns()
        for column in columns:
            print (column.name.lower(), fields)
            if column.name.lower() not in fields:
                column.hidden = True
        config.setColumns(columns)
        self.setAttributeTableConfig(config)

    def load(self, reader):
        super(PEILayer, self).load(reader)

        with open(self._attributesCSVFile()) as fd:
            fields = list(map(lambda x: x.lower(), fd.read().splitlines()))
            self._setShownFields(fields)
