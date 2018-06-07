"""
/***************************************************************************
                             A QGIS Safecast Plugin
                             ----------------------
        begin                : 2016-05-25
        git sha              : $Format:%H$
        copyright            : (C) 2016-2018 by OpenGeoLabs s.r.o.
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
from datetime import datetime, timedelta, date
from dateutil import tz

from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QProgressBar

from qgis.core import QgsVectorLayer, QgsField, QgsFeature, \
    QgsGeometry, QgsPoint, QgsVectorFileWriter, QgsFields, \
    QgsCoordinateReferenceSystem, QgsMessageLog, QgsDistanceArea
from qgis.utils import iface, QGis
from qgis.gui import QgsMessageBar

from osgeo import ogr

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
        self.fileName = fileName
        self._layerName = os.path.splitext(os.path.basename(self.fileName))[0]

        self.storageFormat = storageFormat
        
        # import errors
        self._errs = {}

        # define attributes

        # setting up precision causes in QGIS 2 problems when exporing
        # data into other formats, see
        # https://lists.osgeo.org/pipermail/qgis-developer/2017-December/050969.html
        attrbs = [
            # QgsField("ader_microsvh", QVariant.Double, prec=4),
            QgsField("ader_microsvh", QVariant.Double),
            QgsField("time_local", QVariant.String),
            # QgsField("speed_kmph", QVariant.Double, prec=2),
            QgsField("speed_kmph", QVariant.Double),
            QgsField("dose_increment", QVariant.Double),
            QgsField("time_cumulative", QVariant.String),
            QgsField("dose_cumulative", QVariant.Double),
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
        # skip computed attributes
        # - FID (SQLite only)
        # - ader_microsvh
        # - time_local
        # - speed_kmph
        # - dose_increment
        # - time_cumulative
        # - dose_cumulative
        self.skipNumAttrbs = 6
        # two last columns split (hdop + checksum)
        self._validNumAttrbs = len(attrbs) - (self.skipNumAttrbs + 1)

        # create point layer (WGS-84, EPSG:4326)
        super(SafecastLayer, self).__init__('Point?crs=epsg:4326', self._layerName, "memory")

        self._provider = self.dataProvider()

        # set attributes
        self._provider.addAttributes(attrbs)
        self.updateFields()

        # metadata
        self.setAttribution('Safecast plugin')
        self.setAttributionUrl('https://opengeolabs.github.io/qgis-safecast-plugin')

        # layer is empty, no data loaded
        self._loaded = False
        self.metadata = None

    def setAliases(self):
        """Set aliases
        """
        aliases = [
            self.tr("ADER (microSv/h)"),
            self.tr("Local time"),
            self.tr("Speed (km/h)"),
            self.tr("Increment DOSE"),
            self.tr("Cumulative time"),
            self.tr("Cumulative DOSE"),
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
        if self.storageFormat == "ogr":
            aliases.insert(0, self.tr("FID"))

        for i in range(0, len(aliases)):
            self.addAttributeAlias(i, aliases[i])

    def load(self, reader):
        """Load LOG file using specified reader.

        SafecastReaderError is raised on failure.

        :param reader: reader class used for reading input data
        """
        if self._loaded:
            return # data already loaded

        # store metadata
        self.metadata = {
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

        self.startEditing()
        for f in reader:
            i += 1

            if len(f) < 1:
                # skip empty lines
                continue

            feat = self._processRow(f, i, prev) # process feature
            if feat:
                prev = feat # remember feature for a next run
                feat.setFeatureId(i)
                self.addFeature(feat)

            if i % 100 == 0:
                percent = i / float(count) * 100
                progress.setValue(percent)

        # add features (attributes recalculated)
        self.commitChanges()

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
                        self.fileName, self._errs[attr], attr
                    ),
                    tag='Safecast'
                )

        if self.storageFormat == "ogr":
            # write data into SQLite DB
            self._writeToSQLite()
            self.reload()

        # finish import
        endtime = time.clock() - start
        progress.setValue(100)
        iface.messageBar().clearWidgets()

        # inform user about successful import
        iface.messageBar().pushMessage(
            self.tr("Info"),
            self.tr("{} features loaded (in {:.2f} sec).").format(self.featureCount(), endtime),
            level=QgsMessageBar.INFO,
            duration=3
        )

        # data loaded (avoid multiple imports)
        self._loaded = True

        # switch to read-only mode
        self.setReadOnly(True)

    def _writeToSQLite(self):
        filePath = os.path.splitext(self.fileName)[0] + '.sqlite'
        writer = QgsVectorFileWriter.writeAsVectorFormat(
            self,
            filePath,
            self._provider.encoding(),
            self._provider.crs(),
            "SQLite"
        )
        # TODO: QgsVectorFileWriter.WriterError
        if writer != 0:
            raise SafecastReaderError(self.tr("Unable to create SQLite datasource"))

        # set datasource to SQLite DB
        self.setDataSource(filePath, self._layerName, self.storageFormat)
        self._provider = self.dataProvider()

        # create metadata layer
        ds = ogr.Open(filePath, True)
        layer_name = 'safecast_metadata'
        layer = ds.GetLayerByName(layer_name)
        if layer is None:
            layer = ds.CreateLayer(layer_name, None, ogr.wkbNone)
        layer_defn = layer.GetLayerDefn()
        for key in self.metadata.keys():
            field = ogr.FieldDefn(key, ogr.OFTString)
            layer.CreateField(field)

        feat = ogr.Feature(layer_defn)
        for key, value in self.metadata.items():
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

    def _processRow(self, row, rowid, prev):
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
            self._addError('HDOP = 9999')
            return None
        # - SAT (row[-3])
        if int(row[-3]) < 3:
            self._addError('SAT < 3')
            return None
        ### Date validity will be performed when whole file loaded
        # - year (row[2])
        # myear = datetime2year(row[2])
        # minyear = 2011
        # maxyear = datetime.now().year
        # if myear < minyear or myear > maxyear:
        #     self._addError('year <> {0}-{1}'.format(
        #         minyear, maxyear
        #     ))
        #     return None

        # check timestamp (hours only, dates are fixed when
        # recalculating attributes) validity
        try:
            datetime.strptime(row[2].split('T', 1)[1], "%H:%M:%SZ")
        except ValueError as e:
            self._addError('invalid timestamp {}'.format(row[2]))
            return None

        # - null island
        if abs(x) < sys.float_info.epsilon or \
           abs(y) < sys.float_info.epsilon:
            self._addError('null island')
            return None

        # compute ader_microSvh
        try:
            pulse5s = int(row[4])
            if pulse5s > 0:
                ader = pulse5s * 12
            else:
                ader = int(row[3]) # cpm
            ader *= 0.0029940119760479
        except ValueError:
            ader = -1
        # workaround: setting up precision causes in QGIS 2
        # problems when exporing data into other formats, see
        # https://lists.osgeo.org/pipermail/qgis-developer/2017-December/050969.html
        # disabled
        # see https://bitbucket.org/opengeolabs/qgis-safecast-plugin-dev/issues/14/decrease-the-number-of-decimal-places-in
        # row.insert(0, float('{0:.4f}'.format(ader)))
        row.insert(0, ader)

        # local time will be calculated after loading whole file
        row.insert(1, None)

        # speed will be calculated after loading whole file
        row.insert(2, None)

        # dose increment + time/dose cumulative will be calculated after loading whole file
        row.insert(3, None)
        row.insert(4, None)
        row.insert(5, None)

        # create new feature
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(point))

        # set attributes
        fet.setAttributes(row)

        return fet

class SafecastLayerHelper(object):
    def __init__(self, layer):
        self._layer = layer
        if isinstance(layer, SafecastLayer):
            self._storageFormat = layer.storageFormat
            self._skipNumAttrbs = 7 if self._storageFormat == 'ogr' else 6
            self._fileName = layer.fileName
        else:
            # assuming SQLite (ogr)
            self._storageFormat = "ogr"
            # better to be stored in metadata than hardcoded
            self._skipNumAttrbs = 7
            self._fileName = layer.dataProvider().dataSourceUri().split('|')[0]

        # ader statistics
        self._updateStats()

        # ader plot
        self._plot = [[], []]

        # create object for distance computation
        self._distance = QgsDistanceArea()
        self._distance.setEllipsoidalMode(True)
        self._distance.setEllipsoid('WGS84')

        # connects
        # self._layer.beforeCommitChanges.connect(self.recalculateAttributes)

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

    def _gpsChecksum(self, row):
        """Compute checksum of row.

        :param row: row line

        :return: checksum
        """
        chk = ord(row[0])

        for ichk in row[1:]:
            chk ^= ord(ichk)

        return hex(chk)[2:].upper()

    def _getMetadata(self):
        """Get metadata."""
        if isinstance(self._layer, SafecastLayer):
            return self._layer.metadata

        metadata = {}
        try:
            ds = ogr.Open(self._fileName)
            layer = ds.GetLayerByName('safecast_metadata')
            if layer:
                layer_defn = layer.GetLayerDefn()
                layer.ResetReading()
                feat = layer.GetNextFeature()
                for i in range(layer_defn.GetFieldCount()):
                    name = layer_defn.GetFieldDefn(i).GetName()
                    value = feat.GetField(i)
                    metadata[name] = value
            ds = None
        except:
            raise SafecastReaderError(
                self.tr("Unable to retrive Safecast metadata for selected layer")
            )

        return metadata
        
    def save(self, filePath):
        """Save layer to a new LOG file.

        Raises SafecastWriterError on failure.

        :param filePath: name for output file
        """
        try:
            with open(filePath, 'w') as f:
                f.write('# NEW LOG\n')
                metadata = self._getMetadata()
                f.write('# format={}\n'.format(metadata['format']))
                f.write('# deadtime={}\n'.format(metadata['deadtime']))
                features = self._layer.getFeatures()
                for feat in features:
                    attrs = feat.attributes()
                    row = ''
                    for val in attrs[self._skipNumAttrbs:-2]: # skip calculated points
                        row += '{},'.format(val)
                    row += '{}'.format(attrs[-2])
                    # join two last columns(hdop+checksum)
                    checksum = self._gpsChecksum(row[1:]) # skip '$'
                    row += '*{}\n'.format(checksum)
                    f.write(row)
        except IOError as e:
            raise SafecastWriterError(e)

    def _updateStats(self, data=None):
        """Update ader statistics.

        :param ader: ader statistics
        """
        if data:
            self._stats = data
        else:
            self._stats = {
                'count' : 0,
                'radiation': {
                    'max' : None,
                    'avg' : None,
                    'total': None,
                },
                'route': {
                    'speed' : None,
                    'time': None,
                    'distance' : None,
                }
            }

    def stats(self):
        """Get layer statistics"""
        return self._stats

    def plotData(self):
        return self._plot

    def _validateDate(self, feat_datetime, prev_datetime, first_valid_date):
        """Validate date.

        :param feat_datetime: date to be validated
        :param prev_datetime: previous date or None
        :param first_valid_date: first valid date (if prev_datetime is None)

        :return: validate date, update flag
        """
        if self._checkDate(feat_datetime):
            return feat_datetime, False

        if prev_datetime:
            timediff = self._datetimediff(
                prev_datetime, feat_datetime, timeonly=True
            ).total_seconds()
            fdate = datetime.strptime(
                prev_datetime, "%Y-%m-%dT%H:%M:%SZ"
            ).date()
        else:
            timediff = 0
            fdate = first_valid_date

        if timediff < 0:
            # next date
            fdate += timedelta(days=1)

        return datetime.strftime(
            datetime.combine(
                fdate,
                datetime.strptime(feat_datetime.split('T', 1)[1], "%H:%M:%SZ").time()
            ),
            '%Y-%m-%dT%H:%M:%SZ'
        ), True

    def _datetime2localtime(self, datetime_value):
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

    def _checkDate(self, fdate):
        """Check if date is valid.

        :param fdate: date to be checked

        :return: True if date is valid otherwise False
        """
        minyear = 2011
        maxyear = datetime.now().year
        myear = self._datetime2year(fdate)
        if myear < minyear or myear > maxyear:
            return False
        return True

    def _datetime2year(self, datetime_value):
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

    def _datetimediff(self, datetime_value1, datetime_value2, timeonly=False):
        """Compute datetime difference in sec.

        :param datetime_value1: first value
        :param datetime_value2: second value

        :return: time difference in sec
        """
        if timeonly:
            t1 = datetime.strptime(datetime_value1.split('T', 1)[1], '%H:%M:%SZ')
            t2 = datetime.strptime(datetime_value2.split('T', 1)[1], '%H:%M:%SZ')
            val1 = datetime.combine(date.today(), t1.time())
            val2 = datetime.combine(date.today(), t2.time())
        else:
            val1 = datetime.strptime(datetime_value1, '%Y-%m-%dT%H:%M:%SZ')
            val2 = datetime.strptime(datetime_value2, '%Y-%m-%dT%H:%M:%SZ')

        return val2 - val1

    def recalculateAttributes(self, only_stats=False):
        """Update attributes after loading or editing.

        :param only_stats: True for dry run (do not update attributes, only stats computed)
        """
        def td2str(td):
            """Convert timedelta objects to a HH:MM string with (+/-) sign

            Taken from: https://stackoverflow.com/questions/538666/python-format-timedelta-to-string
            """
            tdhours, rem = divmod(td.total_seconds(), 3600)
            tdminutes, rem = divmod(rem, 60)

            return '{0:02d}:{1:02d}:{2:02d}'.format(
                int(tdhours), int(tdminutes), int(rem)
            )

        # skip FID column for SQLite storage
        idx = 1 if check_version() and self._storageFormat == "ogr" else 0

        dose_inc_idx = self._layer.fieldNameIndex("dose_increment")
        time_cum_idx = self._layer.fieldNameIndex("time_cumulative")
        dose_cum_idx = self._layer.fieldNameIndex("dose_cumulative")
        speed_idx = self._layer.fieldNameIndex("speed_kmph")
        time_local_idx = self._layer.fieldNameIndex("time_local")
        datetime_idx = self._layer.fieldNameIndex("date_time")

        prev = None     # previous feature

        dose_inc = None
        time_cum = 0
        dose_cum = None
        timediff = None
        speed = None
        count = 0

        # fix first valid datetime
        first_valid_date = None
        iter = self._layer.getFeatures()
        for feat in iter:
            fdate_time = feat.attribute("date_time")
            if self._checkDate(fdate_time):
                first_valid_date = datetime.strptime(fdate_time, "%Y-%m-%dT%H:%M:%SZ").date()
                break

        if first_valid_date is None:
            iface.messageBar().pushMessage(
                self._layer.tr("Warning"),
                self._layer.tr("No valid date found. Unable to fix datetime."),
                level=QgsMessageBar.WARNING,
                duration=5
            )

        if not only_stats:
            self._layer.setReadOnly(False)
            self._layer.startEditing()

        prev_datetime = None
        iter = self._layer.getFeatures()

        ader_max = None
        ader_cum = 0
        speed_cum = 0
        dist_cum = 0
        self._plot = [[], []]
        start = time.clock()
        for feat in iter:
            feat_datetime = feat.attribute("date_time")
            # fix date if invalid
            feat_datetime, newdt = self._validateDate(feat_datetime, prev_datetime, first_valid_date)

            # compute ader stats
            ader = feat.attribute("ader_microsvh")
            if ader_max is None or ader_max < ader:
                ader_max = ader
            ader_cum += ader

            # compute local time (from datetime)
            try:
                time_local = self._datetime2localtime(feat_datetime)
            except ValueError:
                time_local = self._layer.tr("unknown")

            if prev:
                timediff = self._datetimediff(
                    prev_datetime,
                    feat_datetime
                ).total_seconds() / (60 * 60)

                dose_inc = ader * timediff

                # speed
                dist = self._distance.measureLine(
                    feat.geometry().asPoint(),
                    prev.geometry().asPoint()
                )
                dist_cum += dist

                # workaround: setting up precision causes in QGIS 2
                # problems when exporing data into other formats, see
                # https://lists.osgeo.org/pipermail/qgis-developer/2017-December/050969.html
                # disabled
                # see https://bitbucket.org/opengeolabs/qgis-safecast-plugin-dev/issues/14/decrease-the-number-of-decimal-places-in
                # speed = float('{0:.2f}'.format((dist / 1e3) / timediff)) # kmph
                speed = (dist / 1e3) / timediff # kmph
                speed_cum += speed

                # time cumulative
                time_cum += timediff

            if dose_inc:
                if dose_cum is None:
                    dose_cum = 0
                dose_cum += dose_inc


            # set previous feature for next run
            prev = feat
            prev_datetime = feat_datetime

            # update plot data
            self._plot[0].append(dist_cum / 1000) # km
            self._plot[1].append(ader)

            # update attributes
            attrs = { dose_inc_idx: dose_inc,
                      time_cum_idx: td2str(timedelta(hours=time_cum)),
                      dose_cum_idx: dose_cum,
                      speed_idx: speed,
                      time_local_idx: time_local,
            }
            if newdt:
                attrs[datetime_idx] = feat_datetime

            count += 1
            if only_stats:
                continue

            for idx, value in attrs.items():
                self._layer.changeAttributeValue(feat.id(), idx, value)

        # update layer internal statistics
        if count > 0:
            self._updateStats({
                'count' : count,
                'radiation': {
                    'max' : ader_max,
                    'avg' : ader_cum / count,
                    'total': dose_cum,
                },
                'route': {
                    'speed' : speed_cum / count,
                    'time': td2str(timedelta(hours=time_cum)),
                    'distance' : dist_cum,
                }
            })
        else:
            self._updateStats()

        # save changes
        if not only_stats:
            self._layer.commitChanges()
            self._layer.setReadOnly(True)

            # force reload attributes
            self._layer.dataProvider().forceReload()

            QgsMessageLog.logMessage('{}: {} features updated in {} sec'.format(
                self._layer.name(), self._layer.featureCount(), time.clock() - start),
                                     tag='Safecast'
            )

    def computeStats(self):
        self.recalculateAttributes(only_stats=False)
