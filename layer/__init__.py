import os
import time

from qgis.PyQt import QtWidgets

from qgis.utils import iface, Qgis
from qgis.core import QgsVectorLayer

class LayerBase(QgsVectorLayer):
    """QGIS layer base class (read-only memory based).
    """
    def __init__(self, filepath):
        self._filepath = filepath
        self._layerName = os.path.splitext(os.path.basename(self._filepath))[0]

        # create point layer (WGS-84, EPSG:4326)
        super(LayerBase, self).__init__('Point?crs=epsg:4326', self._layerName, "memory")

        # layer is empty, no data loaded
        self._loaded = False

    def load(self, reader):
        """Load input data by specified reader.

        :param reader: reader class used for reading input data
        """
        if self._loaded:
            return # data already loaded

        # create progress bar widget
        progressMessageBar = iface.messageBar().createMessage(self.tr("Loading data..."))
        progress = QtWidgets.QProgressBar()
        progress.setMaximum(100)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)

        # load items as new point features (inform user about progress)
        i = 0
        count = reader.count()
        start = time.clock()
        prev = None # previous feature

        self.startEditing()
        for feat in reader:
            print (feat)
            i += 1

            feat.setId(i)
            self.addFeature(feat)

            if i % 100 == 0:
                percent = i / float(count) * 100
                progress.setValue(percent)

        # add features (attributes recalculated)
        self.commitChanges()

        # finish import
        endtime = time.clock() - start
        progress.setValue(100)
        iface.messageBar().clearWidgets()

        # inform user about successful import
        iface.messageBar().pushMessage(
            self.tr("Success"),
            self.tr("{} features loaded (in {:.2f} sec).").format(self.featureCount(), endtime),
            level=Qgis.Success,
            duration=3
        )

        # data loaded (avoid multiple imports)
        self._loaded = True

        # switch to read-only mode
        self.setReadOnly(True)
