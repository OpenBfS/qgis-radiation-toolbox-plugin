import os
import sys
import time
import inspect
import csv
import copy
from enum import Enum

from PyQt5 import QtWidgets
from PyQt5.QtCore import QVariant

from qgis.utils import iface, Qgis
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsMessageLog, QgsField

from osgeo import ogr

from .exceptions import LoadError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from plugin_type import PLUGIN_NAME

class LayerType(Enum):
    Safecast = 0
    ERS = 1
    PEI = 2

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

        self._aliases = [] # list of attribute aliases
        self._provider = self.dataProvider()

        # import errors
        self._errs = {}

        # layer is empty, no data loaded
        self._loaded = False
        self.metadata = None

        # layer type not defined
        self.layerType = None

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

            if i == 1 and not self._aliases:
                # set attributes from data item if needed
                self._aliases = self._setAttrbsDefs(
                    limit=item.keys(),
                    defs=reader.attributeDefs()
                )
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

        if self.storageFormat != "memory":
            self._writeToOgrDataSource()
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

    def _writeToOgrDataSource(self):
        fileExt = self.storageFormat.lower()
        filePath = os.path.splitext(self._fileName)[0] + '.{}'.format(fileExt)
        writer, msg = QgsVectorFileWriter.writeAsVectorFormat(
            self,
            filePath,
            self._provider.encoding(),
            self._provider.crs(),
            driverName=self.storageFormat
        )
        if writer != QgsVectorFileWriter.NoError:
            raise LoadError(
                self.tr("Unable to create SQLite datasource: {}").format(msg)
            )

        # set datasource to new OGR datasource
        self.setDataSource(filePath, self._layerName, 'ogr')
        self._provider = self.dataProvider()

        # create metadata layer
        if self.metadata and 'table' in self.metadata:
            ds = ogr.Open(filePath, True)
            layer_name = self.metadata['table']
            layer = ds.GetLayerByName(layer_name)
            if layer is None:
                layer = ds.CreateLayer(layer_name, None, ogr.wkbNone)
            layer_defn = layer.GetLayerDefn()
            if 'columns' in self.metadata:
                for key in self.metadata['columns']:
                    field = ogr.FieldDefn(key, ogr.OFTString)
                    layer.CreateField(field)

                feat = ogr.Feature(layer_defn)
                for key, value in list(self.metadata['columns'].items()):
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

    def _setAttrbsDefs(self, limit=[], defs=None):
        """Set attributes definition from CSV file if available.

        :param limit: limit to list of attributes

        :returns: list of aliases
        """
        def addAttribute(row, attrbs, aliases):
            attrbs.append(QgsField(
                row['attribute'], eval("QVariant.{}".format(row['qtype']))
            ))
            aliases.append(row['alias'].replace('_', ' '))

        def processAttributes(csv_attrbs, limit):
            attrbs = []
            aliases = []

            if limit:
                # limit attributes based on input file (first feature) - ERS format specific
                for name in limit:
                    # first try full name match
                    found = False
                    for row in csv_attrbs:
                        if row['attribute'] == name:
                            addAttribute(row, attrbs, aliases)
                            found = True
                            break
                    if found:
                        continue
                    for row in csv_attrbs:
                        # full name match is not required see
                        # https://gitlab.com/opengeolabs/qgis-radiation-toolbox-plugin/issues/41#note_136183930
                        if row['attribute'] == name[:len(row['attribute'])] or name == row['attribute'][:len(name)]:
                            row_modified = copy.copy(row)
                            row_modified['attribute'] = name # force (full) attribute name from input file
                            if row_modified['alias']:
                                row_modified['alias'] = '{} ({})'.format(name, row_modified['alias'])
                            addAttribute(row_modified, attrbs, aliases)
                            break
            else:
                # add all attributes
                for row in csv_attrbs:
                    addAttribute(row, attrbs, aliases)

            return attrbs, aliases

        if not defs:
            # predefined attributes (CSV file)
            # Safecast, ERS
            csv_file = os.path.join(
                os.path.dirname(__file__),
                os.path.splitext(inspect.getfile(self.__class__))[0] + '.csv')
            if not os.path.exists(csv_file):
                return []

            with open(csv_file) as fd:
                csv_attrbs = list(csv.DictReader(fd, delimiter=';'))
                attrbs, aliases = processAttributes(csv_attrbs, limit)
        else:
            # data-related attributes
            # PEI
            attrbs, aliases = processAttributes(defs, limit)

        if limit:
            if len(attrbs) != len(limit):
                raise LoadError(
                    "Number of attributes differs {} vs {}".format(
                        len(attrbs), len(limit)
                ))

        if aliases and self.storageFormat != "memory":
            aliases.insert(0, "FID")

        # set attributes
        self._provider.addAttributes(attrbs)
        self.updateFields()

        return aliases

    def setAliases(self):
        """Set aliases
        """
        for i in range(0, len(self._aliases)):
            self.setFieldAlias(i, self._aliases[i])
