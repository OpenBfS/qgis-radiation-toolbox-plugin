import os
from collections import OrderedDict

from . import ReaderBase
from .exceptions import ReaderError

from qgis.core import QgsFeature, QgsPointXY, QgsGeometry

class ERSReader(ReaderBase):
    """ERS reader class.
    """
    def __init__(self, filepath):
        super(ERSReader, self).__init__(filepath)

    def _next_data_item(self):
        """Read next data item.
        """
        while True:
            line = self._fd.readline().rstrip(os.linesep)
            if not line:
                # EOF
                return None
            if line.startswith('PA '):
                item = OrderedDict()
                for it in line.split(';'):
                    k, v = it.split(' ', 1)
                    item[k] = v

                return item

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
        ### feat.setAttributes(list(item.values()))

        return feat

    def count(self):
        """Count data items.

        Inspired by http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python.
        """
        self._reset()

        lines = 0
        buf_size = 1024 * 1024
        read_f = self._fd.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('PA ')
            buf = read_f(buf_size)

        return lines
