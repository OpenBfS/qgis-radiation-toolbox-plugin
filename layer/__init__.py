import os
import sys
import time

from PyQt5 import QtWidgets

from qgis.utils import iface, Qgis
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsMessageLog

from osgeo import ogr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from plugin_type import PLUGIN_NAME

class LayerBase(QgsVectorLayer):
    """QGIS layer base class (read-only memory based).

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
    """
    def __init__(self, fileName, storageFormat):
        self._fileName = fileName
        self._layerName = os.path.splitext(os.path.basename(self._fileName))[0]
        self.storageFormat = storageFormat
        
        # create point layer (WGS-84, EPSG:4326)
        super(LayerBase, self).__init__('Point?crs=epsg:4326', self._layerName, "memory")

        self._provider = self.dataProvider()

        # import errors
        self._errs = {}

        # layer is empty, no data loaded
        self._loaded = False
        self.metadata = None

    def load(self, reader):
        """Load input data by specified reader.

        :param reader: reader class used for reading input data
        """
        if self._loaded:
            return # data already loaded

        # create progress bar widget
        progressMessageBar = iface.messageBar().createMessage(
            self.tr("Loading data...")
        )
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
        for item in reader:
            i += 1

            feat = self._item2feat(item)
            if not feat:
                # error appeared
                continue
            feat.setId(i)
            self.addFeature(feat)

            if i % 100 == 0:
                percent = i / float(count) * 100
                progress.setValue(percent)

        # add features (attributes recalculated if requested)
        self.commitChanges()

        if self.storageFormat == "ogr":
            # write data into SQLite DB
            self._writeToSQLite()
            self.reload()

        # finish import
        endtime = time.clock() - start
        progress.setValue(100)
        iface.messageBar().clearWidgets()

        if self._errs:
            # report errors if any
            iface.messageBar().pushMessage(
                self.tr("Warning"),
                self.tr("{} invalid measurement(s) skipped (see message log for details)").format(
                    sum(self._errs.values())
                ),
                level=Qgis.Warning,
                duration=5
            )

            for attr in list(self._errs.keys()):
                QgsMessageLog.logMessage(
                    "{}: {} measurement(s) skipped (invalid {})".format(
                        self._fileName, self._errs[attr], attr
                    ),
                    tag=PLUGIN_NAME
                )
        
        # inform user about successful import
        iface.messageBar().pushMessage(
            self.tr("Data loaded"),
            self.tr("{} features loaded (in {:.2f} sec).").format(self.featureCount(), endtime),
            level=Qgis.Success,
            duration=3
        )

        # data loaded (avoid multiple imports)
        self._loaded = True

        # switch to read-only mode
        self.setReadOnly(True)

    def _writeToSQLite(self):
        filePath = os.path.splitext(self._fileName)[0] + '.sqlite'
        writer, msg = QgsVectorFileWriter.writeAsVectorFormat(
            self,
            filePath,
            self._provider.encoding(),
            self._provider.crs(),
            driverName="SQLite"
        )
        if writer != QgsVectorFileWriter.NoError:
            raise ReaderError(
                self.tr("Unable to create SQLite datasource: {}").format(msg)
            )

        # set datasource to SQLite DB
        self.setDataSource(filePath, self._layerName, self.storageFormat)
        self._provider = self.dataProvider()

        # create metadata layer
        if self.metadata:
            ds = ogr.Open(filePath, True)
            layer_name = '{}_metadata'.format(self.__class__.__name__.lower())
            layer = ds.GetLayerByName(layer_name)
            if layer is None:
                layer = ds.CreateLayer(layer_name, None, ogr.wkbNone)
            layer_defn = layer.GetLayerDefn()
            for key in list(self.metadata.keys()):
                field = ogr.FieldDefn(key, ogr.OFTString)
                layer.CreateField(field)

            feat = ogr.Feature(layer_defn)
            for key, value in list(self.metadata.items()):
                feat.SetField(key, value)
            layer.CreateFeature(feat)
            feat = None

    def _addError(self, etype):
        """Add error message.

        :param etype: error type (HDOP, SAT, ...)
        """
        if etype not in self._errs:
            self._errs[etype] = 0
        self._errs[etype] += 1

    def _item2feat(self, item):
        """Create QgsFeature from data item.
        """
        raise NotImplementedError()

