"""
/***************************************************************************
                             A QGIS Safecast Plugin
                             ----------------------
        begin                : 2016-05-25
        git sha              : $Format:%H$
        copyright            : (C) 2016-2017 by OpenGeoLabs s.r.o.
        acknowledgement      : Suro, Czech Republic
        email                : martin.landa@opengeolabs.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys
import time
from datetime import datetime
from dateutil import tz

from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QProgressBar

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, \
    QgsGeometry, QgsPoint, QgsVectorFileWriter, QgsFields, \
    QgsCoordinateReferenceSystem, QgsMessageLog, QgsDistanceArea
from qgis.utils import iface, QGis
from qgis.gui import QgsMessageBar

from .reader import SafecastReaderError

def check_version(min_version=(2,18)):
    version = map(int, QGis.QGIS_VERSION.split('.')[:2])
    if version[0] >= min_version[0] and version[1] >= min_version[1]:
        return True

    return False

class SafecastWriterError(Exception):
    """Safecast writer error class.
    """
    pass

class SafecastLayer(QgsVectorLayer):
    def __init__(self, fileName, storageFormat):
        """Safecast memory-based read-only layer.

        :param fileName: path to input file
        :param storageFormat: storage format for layer (Memory or SQLite)
        """
        self._fileName = fileName
        self._storageFormat = storageFormat

        # ader statistics
        self._stats = { 'min': None,
                        'max': None,
                        'count': 0,
                        'sum': 0,
                        'mean': None }

        # ader plot
        self._plot = []

        # import errors
        self._errs = {}

        # create object for distance computation
        self._distance = QgsDistanceArea()
        self._distance.setEllipsoidalMode(True)
        self._distance.setEllipsoid('WGS84')

        # define attributes
        attrbs = [
            QgsField("ader_microsvh", QVariant.Double),
            QgsField("dose_current", QVariant.Double),
            QgsField("dose_cumulative", QVariant.Double),
            QgsField("time_local", QVariant.String),
            QgsField("speed", QVariant.String),
            QgsField("device", QVariant.String),
            QgsField("device_id",  QVariant.Int),
            QgsField("date_time", QVariant.String),
            QgsField("cpm", QVariant.Int),
            QgsField("pulses5s", QVariant.Int),
            QgsField("pulses_total", QVariant.Int),
            QgsField("validity", QVariant.String),
            QgsField("lat_deg", QVariant.String),
            QgsField("hemisphere", QVariant.String),
            QgsField("long_deg", QVariant.String),
            QgsField("east_west", QVariant.String),
            QgsField("altitude", QVariant.Double),
            QgsField("gps_validity", QVariant.String),
            QgsField("sat", QVariant.Int),
            QgsField("hdop", QVariant.Int),
            QgsField("checksum", QVariant.String)
        ]
        # four columns (fid, ader_microSvh, dose_current, dose_cumulative, time_local, speed, hdop, checksum) are computed
        self._validNumAttrbs = len(attrbs) - 6

        # create point layer (WGS-84, EPSG:4326)
        layerName = os.path.splitext(os.path.basename(self._fileName))[0]
        if self._storageFormat == "ogr":
            from osgeo import ogr, osr
            filePath = os.path.splitext(self._fileName)[0] + '.sqlite'
            fileName = "{}|layername={}|geometrytype=Point".format(
                filePath, layerName
            )

            # rewrite output DB if exists
            if os.path.exists(filePath):
                os.remove(filePath)

            # new DB with empty layer must be created before reading
            # layer
            driver = ogr.GetDriverByName("SQLite")
            dataSource = driver.CreateDataSource(filePath)
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            layer = dataSource.CreateLayer(str(layerName), srs, ogr.wkbPoint)
            dataSource = None # write changes
        else:
            fileName = 'Point?crs=epsg:4326'
        super(SafecastLayer, self).__init__(fileName, layerName, self._storageFormat)

        self._provider = self.dataProvider()

        # set aliases when running QGIS 2.18+
        if check_version():
            self._setAliases(attrbs)

        # set attributes
        self._provider.addAttributes(attrbs)
        self.updateFields()

        # layer is empty, no data loaded
        self._loaded = False

    def _setAliases(self, attrbs):
        """Set aliases

        :params attrbs: list of QgsField instances
        """
        alias = [
            self.tr("ADER microSv/h"),
            self.tr("Current DOSE"),
            self.tr("Cumulative DOSE"),
            self.tr("Local time"),
            self.tr("Speed"),
            self.tr("Device"),
            self.tr("Device ID"),
            self.tr("Datetime"),
            self.tr("CPM"),
            self.tr("Pulses 5sec"),
            self.tr("Pulses total"),
            self.tr("Validity"),
            self.tr("Latitude (deg)"),
            self.tr("Hemisphere"),
            self.tr("Longitude (deg)"),
            self.tr("East/West"),
            self.tr("Altitude"),
            self.tr("GPS Validity"),
            self.tr("Sat"),
            self.tr("HDOP"),
            self.tr("CheckSum")
        ]
        i = 0
        for field in attrbs:
            field.setAlias(alias[i])
            i += 1

    def load(self, reader):
        """Load LOG file using specified reader.

        SafecastReaderError is raised on failure.

        :param reader: reader class used for reading input data
        """
        if self._loaded:
            return # data already loaded

        # store metadata
        self._metadata = {
            'format': reader.format_version,
            'deadtime': reader.deadtime
        }

        # create progress bar widget
        progressMessageBar = iface.messageBar().createMessage(self.tr("Loading data..."))
        progress = QProgressBar()
        progress.setMaximum(100)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)

        # load items as new point features (inform user about progress)
        i = 0
        count = reader.count()
        start = time.clock()
        prev = None # previous feature
        # feats = []

        self.startEditing()
        for f in reader:
            i += 1

            feat = self._process_row(f, i, prev) # process feature
            if feat:
                prev = feat # remember feature for a next run
                feat.setFeatureId(i)
                self.addFeature(feat)
                # feats.append(feat)

            if i % 100 == 0:
                percent = i / float(count) * 100
                progress.setValue(percent)

        # add features
        self.commitChanges()
        # self._provider.addFeatures(feats)

        endtime = time.clock() - start
        progress.setValue(100)
        iface.messageBar().clearWidgets()

        # inform user about successful import
        iface.messageBar().pushMessage(
            self.tr("Info"),
            self.tr("{} features loaded (in {:.2f} sec).").format(self._stats['count'], endtime),
            level=QgsMessageBar.INFO,
            duration=3
        )

        if self._errs:
            # report errors if any
            iface.messageBar().pushMessage(
                self.tr("Warning"),
                self.tr("{} invalid measurement(s) skipped (see message log for details)").format(
                    sum(self._errs.values())
                ),
                level=QgsMessageBar.WARNING,
                duration=5
            )

            for attr in self._errs.keys():
                QgsMessageLog.logMessage(
                    "{}: {} measurement(s) skipped (invalid {})".format(
                        self._fileName, self._errs[attr], attr
                    ),
                    level=QgsMessageLog.WARNING
                )

        # data loaded (avoid multiple imports)
        self._loaded = True
        # switch to read-only mode
        self.setReadOnly(True)

    def _add_error(self, etype):
        """Add error message.

        :param etype: error type (HDOP, SAT, ...)
        """
        if etype not in self._errs:
            self._errs[etype] = 0
        self._errs[etype] += 1

    def _process_row(self, row, rowid, prev):
        """Process line in LOG file and create a new point feature based on this line.

        :param row: row to be processed
        :param rowid: force feature id
        :param prev: previous feature for cumulative values
        """
        # define internal functions first
        def coords_float(coord, ne):
            """Convert coordinates to DMS.

            :param coord: coordinates as a string
            :param ne: longitude/latitude indicator

            :return: coordinate value
            """
            ddmm, s = coord.split('.', 1)
            val = int(ddmm[:-2]) + int(ddmm[-2:])/60. + float('0.'+s)/60.
            if ne in ('S', 'W'):
                val *= -1
            return val

        def datetime2localtime(datetime_value):
            """Convert datetime value to local time.

            :datetime_value: date time value (eg. '2016-05-16T18:22:26Z')

            :return: local time as a string (eg. '20:22:26')
            """
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()

            utc = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%SZ')
            utc = utc.replace(tzinfo=from_zone)
            local = utc.astimezone(to_zone)

            return local.strftime('%H:%M:%S')

        def datetime2year(datetime_value):
            """Convert datatime value to year.

            :datetime_value: date time value (eg. '2016-05-16T18:22:26Z')

            :return: local time as a int (2016)
            """
            try:
                return datetime.strptime(
                    datetime_value, '%Y-%m-%dT%H:%M:%SZ'
                ).year
            except ValueError:
                return 0

        def datetimediff(datetime_value1, datetime_value2):
            """Compute datetime difference in sec.

            :param datetime_value1: first value
            :param datetime_value2: second value

            :return: time difference in sec
            """
            val1 = datetime.strptime(datetime_value1, '%Y-%m-%dT%H:%M:%SZ')
            val2 = datetime.strptime(datetime_value2, '%Y-%m-%dT%H:%M:%SZ')

            return val2 - val1

        if len(row) != self._validNumAttrbs:
            raise SafecastReaderError(self.tr("Failed to read input data. Line: {}").format(','.join(row)))

        # force to split last item (hdop & checksum)
        row[-1], newitem = row[-1].split('*', 1)
        row.append('*' + newitem)

        # set coordinates
        y = coords_float(row[7], row[8])
        x = coords_float(row[9], row[10])
        point = QgsPoint(x, y)

        # check validity
        # drop data according
        # - HDOP (row[-2])
        if int(row[-2]) == 9999:
            self._add_error('HDOP = 9999')
            return None
        # - SAT (row[-3])
        if int(row[-3]) < 3:
            self._add_error('SAT < 3')
            return None
        # - year (row[2])
        myear = datetime2year(row[2])
        minyear = 2011
        maxyear = datetime.now().year
        if myear < minyear or myear > maxyear:
            self._add_error('year <> {0}-{1}'.format(
                minyear, maxyear
            ))
            return None
        # - null island
        if abs(x) < sys.float_info.epsilon or \
           abs(y) < sys.float_info.epsilon:
            self._add_error('null island')
            return None

        # compute ader_microSvh
        try:
            ader = int(row[3]) * 0.0028571429
        except ValueError:
            ader = -1
        row.insert(0, ader)
        # update statistics
        self._update_stats(ader)

        # TODO: find better approach
        idx = 1 if check_version() and self._storageFormat == "ogr" else 0
        # compute current dose
        row.insert(1, ader if not prev else (prev[0+idx] + ader if prev[0+idx] == prev[1+idx] else ader))
        # compute cumulative dose
        row.insert(2, (prev[2+idx] if prev else 0) + ader)

        # compute local time (from datetime)
        try:
            time_local = datetime2localtime(row[5])
        except ValueError:
            time_local = self.tr("unknown")
        row.insert(3, time_local)

        # compute speed
        if prev:
            dist = self._distance.measureLine(point, prev.geometry().asPoint())
            timediff = datetimediff(
                prev[7+idx],
                row[6]
            ).total_seconds()
            speed = dist / timediff
        else:
            speed = None
        row.insert(4, speed)

        # update plot data
        self._plot.append((time_local, ader))
        
        # create new feature
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(point))

        if check_version() and self._storageFormat == "ogr":
            # force feature id (fix SQLite issue)
            row.insert(0, rowid)

        # set attributes
        fet.setAttributes(row)

        return fet

    def save(self, filePath):
        """Save layer to a new LOG file.

        Raises SafecastWriterError on failure.

        :param filePath: name for output file
        """
        try:
            with open(filePath, 'w') as f:
                f.write('# NEW LOG\n')
                f.write('# format={}\n'.format(self._metadata['format']))
                f.write('# deadtime={}\n'.format(self._metadata['deadtime']))
                features = self.getFeatures()
                for feat in features:
                    attrs = feat.attributes()
                    for val in attrs[2:-2]: # skip ader_microSvh and local time
                        f.write('{},'.format(val))
                    f.write('{}{}\n'.format(attrs[-2], attrs[-1]))
        except IOError as e:
            raise SafecastWriterError(e)

    def path(self):
        """Return layer file directory path.

        :return: path as a string
        """
        return os.path.dirname(self._fileName)

    def filename(self):
        """Return layer file name without extension.

        :return: filename as a string
        """
        return os.path.splitext(
            os.path.basename(self._fileName)
        )[0]

    def _update_stats(self, value):
        """Update ader statistics.

        :param ader: ader statistics
        """
        if self._stats['min'] is None or self._stats['min'] > value:
            self._stats['min'] = value
        if self._stats['max'] is None or self._stats['max'] < value:
            self._stats['max'] = value
        self._stats['sum'] += value
        self._stats['count'] += 1
        self._stats['mean'] = self._stats['sum'] / self._stats['count']

    def stats(self):
        """Get layer statistics"""
        return self._stats

    def plot_data(self):
        def time2float(value):
            h, m, s = map(float, value.split(':'))
            return h + m / 60. + s / 3600.

        x = []
        y = []
        for time_local, ader in self._plot:
            x.append(time2float(time_local))
            y.append(ader)

        return x, y
