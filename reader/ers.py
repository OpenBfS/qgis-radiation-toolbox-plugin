import os
from collections import OrderedDict

from . import ReaderBase
from .exceptions import ReaderError

from qgis.core import QgsFeature, QgsPointXY, QgsGeometry

class ERSReader(ReaderBase):
    """ERS reader class.
    """
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
                    if k == '#S':
                        # see https://gitlab.com/opengeolabs/qgis-radiation-toolbox-plugin/issues/41#note_137813150
                        idx = 1
                        for s_v in v.strip().split(' '):
                            item['{}{}'.format(k, idx)] = s_v
                            idx += 1
                    else:
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
        """
        return self._count('PA ')
