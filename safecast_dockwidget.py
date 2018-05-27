# -*- coding: utf-8 -*-
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
import logging
from collections import OrderedDict
from datetime import datetime, timedelta

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QMessageBox, QToolBar, QGridLayout, QLabel, \
    QSpacerItem, QSizePolicy, QAction
from PyQt4.QtCore import QSignalMapper, SIGNAL, SLOT, pyqtSignal, QSettings

from qgis.core import QgsMapLayerRegistry, QgsProject, QgsRasterLayer
from qgis.gui import QgsMessageBar
from qgis.utils import iface

from osgeo import ogr

from .reader import SafecastReader, SafecastReaderError, SafecastReaderLogger
from .safecast_layer import SafecastLayer, SafecastWriterError, SafecastLayerHelper
from .safecast_stats import SafecastStats
try:
    from .safecast_plot import SafecastPlot
    plotMsg = None
except ImportError as e:
    plotMsg = "Plot functionality not available. Reason: {}".format(e)
    iface.messageBar().pushMessage("Safecast plugin", plotMsg,
                                   level=QgsMessageBar.WARNING, duration=10)

# register logger handler
hdlr = logging.StreamHandler()
# set logger level
SafecastReaderLogger.setLevel(level=logging.INFO)
SafecastReaderLogger.addHandler(hdlr)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'safecast_dockwidget_base.ui'))

class SafecastError(Exception):
    """Safecast generic error class.
    """
    pass

class SafecastDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Plugin constructor.

        :param parent: parent class or None
        """
        super(SafecastDockWidget, self).__init__(parent)
        self.setupUi(self)

        # connect ui with functions
        self._createToolbarAndConnect()

        # actions
        self.actionUpdateStatsPlot = QAction("UpdateStatsPlot", self)

        # generic connects
        iface.currentLayerChanged.connect(self.onUpdatePlugin)
        self.actionUpdateStatsPlot.triggered.connect(self.onUpdateStatsPlot)

        # load internal styles
        self._initStyles()

        # initialize internal variables
        self._initStats()
        self._initPlot()
        self._initMaps()

        # list of layers (must be defined, otherwise SafecastLayer is
        # not returned by getActiveLayer()
        self._layers = {}

        # settings
        self._settings = QSettings()
        self._loadSettings()

    def _createToolbarAndConnect(self):
        """Create toolbar and connect tools."""
        self.signalMapper = QSignalMapper(self)

        self._mToolbar = QToolBar(self)
        self._mToolbar.addAction(self.actionImport)
        self._mToolbar.addAction(self.actionSave)
        self._mToolbar.addSeparator()
        self._mToolbar.addAction(self.actionSelect)
        self._mToolbar.addAction(self.actionDeselect)
        self._mToolbar.addSeparator()
        self._mToolbar.addAction(self.actionDelete)

        self.actionSave.setEnabled(False)
        self.actionSelect.setEnabled(False)
        self.actionDeselect.setEnabled(False)
        self.actionDelete.setEnabled(False)
                
        self.toolbarLayout.insertWidget(0, self._mToolbar)
        
        self.connect(self.actionImport,
                     SIGNAL("triggered()"), self.onLoad)
        self.connect(self.actionSave,
                     SIGNAL("triggered()"), self.onSave)
        self.connect(self.actionSelect,
                     SIGNAL("triggered()"), self.onSelect)
        self.connect(self.actionDeselect,
                     SIGNAL("triggered()"), self.onDeselect)
        self.connect(self.actionDelete,
                     SIGNAL("triggered()"), self.onDelete)
        self.connect(self.styleButton,
                     SIGNAL("clicked()"), self.onStyle)
        self.connect(self.plotStyleCombo,
                     SIGNAL("currentIndexChanged(int)"), self.onPlotStyle)
        self.connect(self.storageCombo,
                     SIGNAL("currentIndexChanged(int)"), self.onStorageFormat)
        self.connect(self.onlineMapsButton,
                     SIGNAL("clicked()"), self.onAddOnlineMap)

    def _loadSettings(self):
        """Load settings."""
        # storage format
        sender = 'safecast-{}-lastCurrentIndex'.format(self.storageCombo.objectName())
        self.storageCombo.setCurrentIndex(int(self._settings.value(sender, 0)))
        # plot style
        sender = 'safecast-{}-lastCurrentIndex'.format(self.plotStyleCombo.objectName())
        self.plotStyleCombo.setCurrentIndex(int(self._settings.value(sender, 0)))

    def _initStyles(self):
        """Define internal styles and polulates items in combobox."""
        self._styles = [
            {'name' : '0.08 - 10.00 microSv/h', 'file' : 'normal'},
            {'name' : '0.05 - 200.00 microSv/h', 'file' : 'high'}
        ]

        for item in self._styles:
            self.styleBox.addItem(item['name'])
        self.styleBox.setCurrentIndex(0)

    def _initStats(self, statsWidget=False):
        """Initialize statistics tab.

        :param statsWidget: True to create plot widget otherwise info
        QLabel is displayed
        """
        # use grid layout
        if not hasattr(self, "_statsLayout"):
            self._statsLayout = QGridLayout(self.groupStats)

        if not hasattr(self, "_statsWidget"):
            self._statsWidget = SafecastStats(self.groupStats)
            self._statsWidget.setHeaderHidden(True)

        if not hasattr(self, "_statsLabel"):
            self._statsLabel = QLabel(
                self.tr("Load or select Safecast layer in order to display ader statistics."),
                self.groupStats
            )
            self._statsSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

            self._statsLayout.addWidget(self._statsLabel)
            self._statsLayout.addItem(self._statsSpacer)
            self._statsWidget.setVisible(False)
            self._statsVisible = False
            return # initialization done

        if statsWidget and not self._statsVisible:
            # remove info label & spacer from layout
            self._statsLabel.setVisible(False)
            self._statsLayout.removeWidget(self._statsLabel)
            self._statsLayout.removeItem(self._statsSpacer)
            # add stats widget into layout
            self._statsWidget.setVisible(True)
            self._statsLayout.addWidget(self._statsWidget)
            self._statsVisible = True

            self.groupStats.adjustSize()

        elif not statsWidget and self._statsVisible:
            # remove plot widget from layout
            self._statsWidget.setVisible(False)
            self._plotLayout.removeWidget(self._statsWidget)
            self._statsVisible = False
            # add info label & spacer into layout
            self._statsLabel.setVisible(True)
            self._statsLayout.addWidget(self._statsLabel)
            self._statsLayout.addItem(self._statsSpacer)
            # set group tile
            self.groupStats.setTitle(self.tr("Statistics"))
        
    def _initPlot(self, plotWidget=False):
        """Initialize plot tab.

        :param plotWidget: True to create plot widget otherwise info
        QLabel is displayed
        """
        # use grid layout if not defined
        if not hasattr(self, "_plotLayout"):
            self._plotLayout = QGridLayout(self.groupPlot)

        # create new plot widget
        if not hasattr(self, "_plotWidget") and not plotMsg:
            self._plotWidget = SafecastPlot(self.groupPlot)
            self._plotWidget.setVisible(False)

        if not hasattr(self, "_plotLabel"):
            self._plotLabel = QLabel(
                self.tr("Load or select Safecast layer in order to display ader plot.")
                if not plotMsg else plotMsg, self.groupPlot)
            self._plotSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

            self._plotLayout.addWidget(self._plotLabel)
            self._plotLayout.addItem(self._plotSpacer)
            self._plotVisible = False
            return # initialization done
        
        if plotWidget and not self._plotVisible:
            # remove info label & spacer from layout
            self._plotLabel.setVisible(False)
            self._plotLayout.removeWidget(self._plotLabel)
            self._plotLayout.removeItem(self._plotSpacer)
            # add plot widget into layout
            self._plotWidget.setVisible(True)
            self._plotLayout.addWidget(self._plotWidget)
            self._plotVisible = True

            self.groupPlot.adjustSize()

        elif not plotWidget and self._plotVisible:
            # remove plot widget from layout
            self._plotWidget.setVisible(False)
            self._plotLayout.removeWidget(self._plotLabel)
            self._plotVisible = False
            # add info label & spacer into layout
            self._plotLabel.setVisible(True)
            self._plotLayout.addWidget(self._plotLabel)
            self._plotLayout.addItem(self._plotSpacer)
            # set group tile
            self.groupPlot.setTitle(self.tr("Plot"))

    def _initMaps(self):
        self._onlineMaps = [
            ("OpenStreetMap", "layers=OSM-WMS&url=http://ows.mundialis.de/services/service?")
        ]
        self._onlineMapsDefaultParams = 'contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&styles=&'

        # add items
        self.onlineMapsCombo.addItems(list(item[0] for item in self._onlineMaps))

    def stylePath(self):
        """Get style path (when local QML files are located).

        :return: path given as a string
        """
        styleName = self._styles[self.styleBox.currentIndex()]['file']
        stylePath = os.path.join(os.path.dirname(__file__), "styles", styleName + '.qml')
        if not os.path.isfile(stylePath):
            raise SafecastError(self.tr("Style '{}' not found").format(styleName))

        return stylePath
    
    def closeEvent(self, event):
        """Close plugin.

        :param event: related event
        """
        self.closingPlugin.emit()
        event.accept()

    def onLoad(self):
        """Load LOG file as a new QGIS point map layer.

        Input LOG file is given by user via open dialog. Loaded point
        layer is symbolized using default internal style. Layer is
        inserted into layer tree (TOC) on first position.

        Shows error dialog on failure.

        """
        # get last used directory path from settings
        sender = 'safecast-{}-lastUserFilePath'.format(self.sender().objectName())
        lastPath = self._settings.value(sender, '')

        filePath = QFileDialog.getOpenFileName(self, self.tr("Load Safecast LOG file"),
                                               lastPath, self.tr("LOG file (*.LOG)"))
        if not filePath:
            # action canceled
            return

        # storage format
        storageFormat = 'ogr' if self.storageCombo.currentIndex() == 0 else 'memory'

        filePath = os.path.normpath(filePath)
        try:
            # create reader for input data
            reader = SafecastReader(filePath)
            # create new QGIS map layer (read-only)
            layer = SafecastLayer(filePath, storageFormat)
            # register new layer in plugin's internal list
            # helper must be assigned before loading data (!)
            self._layers[layer.id()] = SafecastLayerHelper(layer)

            # load data by reader into new layer and set style
            layer.load(reader)
            # set style
            layer.loadNamedStyle(self.stylePath())
            layer.setAliases() # loadNameStyle removes aliases (why?)

            # add map layer to the canvas (do not add into TOC)
            QgsMapLayerRegistry.instance().addMapLayer(layer, False)
            # force register layer in TOC as a first item
            QgsProject.instance().layerTreeRoot().insertLayer(0, layer)
            # select this layer (this must be done manually since we
            # are inserting item into layer tree)
            iface.legendInterface().setCurrentLayer(layer)
            # expand layer
            iface.legendInterface().setLayerExpanded(layer, True)
        except (SafecastError, SafecastReaderError) as e:
            # show error message on failure
            iface.messageBar().clearWidgets()
            QMessageBox.critical(None, self.tr("Error"),
                                 self.tr("Failed to load input file '{0}'.\n\nDetails: {1}").format(
                                     filePath, e), QMessageBox.Abort
            )
            return

        # enable save, select, style buttons when new layer is
        # successfully loaded
        if not self.actionSave.isEnabled():
            self.actionSave.setEnabled(True)
            self.actionSelect.setEnabled(True)
            self.styleButton.setEnabled(True)

        # zoom to the new layer (already selected)
        iface.zoomToActiveLayer()

        # remember directory path
        self._settings.setValue(sender, os.path.dirname(filePath))

    def onPlotStyle(self, idx):
        """Plot style changed.
        """
        # remember style
        sender = 'safecast-{}-lastCurrentIndex'.format(self.sender().objectName())
        self._settings.setValue(sender, idx)

        layer = self.getActiveLayer()
        if not layer:
            # no layer is currently selected, nothing to do
            return

        # re-render plot
        self.updatePlot(layer)

    def onStyle(self):
        """Apply new style for currently selected layer.

        Show error message dialog on failure.
        """
        layer = self.getActiveLayer()
        if not layer:
            # no layer is currently selected, nothing to do
            return

        # apply new style on currently selected layer
        try:
            layer.loadNamedStyle(self.stylePath())
            layer.setAliases() # loadNameStyle removes aliases (why?)
        except SafecastError as e:
            # print error message on failure
            QMessageBox.critical(None, self.tr("Error"),
                                 self.tr("Failed to apply style: {0}").format(
                                     e), QMessageBox.Abort
            )

        # If caching is enabled, a simple canvas refresh might not be sufficient
        # to trigger a redraw and you must clear the cached image for the layer
        if iface.mapCanvas().isCachingEnabled():
            layer.setCacheImage(None)
        else:
            iface.mapCanvas().refresh()
        iface.legendInterface().refreshLayerSymbology(layer)

    def onSave(self):
        """Save currently selected map layer as new LOG file.

        Show error message dialog on failure.
        """
        # get currently selected layer
        layer = self.getActiveLayer()
        helper = self._getLayerHelper(layer)
        if not helper:
                QMessageBox.critical(None, self.tr("Error"),
                                     self.tr("Invalid Safecast layer"),
                                     QMessageBox.Abort
                )

        # overwrite check disabled because of possible missing file extension
        filePath = QFileDialog.getSaveFileName(self, self.tr("Save layer as new LOG file"),
                                               os.path.join(
                                                   helper.path() if layer else ".",
                                                   helper.filename() + '_mod.LOG'
                                               ),
                                               self.tr("LOG file (*.LOG)"),
                                               QFileDialog.DontConfirmOverwrite)
        if not filePath:
            # action canceled
            return

        if not filePath.endswith('.LOG'):
            # add missing extension if missing
            filePath += '.LOG'

        if os.path.exists(filePath):
            # check if the file already exists
            reply = QMessageBox.question(self, self.tr("Overwrite?"),
                                         self.tr("File {} already exists. "
                                                 "Do you want to overwrite it?.").format(filePath),
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply != QtGui.QMessageBox.Yes:
                return

        if layer:
            try:
                # export layer to LOG file
                helper.save(filePath)
            except SafecastWriterError as e:
                QMessageBox.critical(None, self.tr("Error"),
                                     self.tr("Failed to save LOG file: {0}").format(
                                         e), QMessageBox.Abort
                )

    def onSelect(self):
        """Select features action."""
        layer = self.getActiveLayer()
        if not layer:
            # disable select button if no layer selected
            self.actionSelect.setEnabled(False)
            return

        if not self.actionDeselect.isEnabled():
            # enable deselect/delete buttons if features selected
            self.actionDeselect.setEnabled(True)
            self.actionDelete.setEnabled(True)
        iface.actionSelect().trigger()

    def onDeselect(self):
        """Deselect features action."""
        layer = self.getActiveLayer()
        if layer:
            # deselect features manually (there is no trigger
            # available) if requested
            layer.setSelectedFeatures([feat.id() 
                                       for feat in layer.selectedFeaturesIterator() if feat.id() < 0])
        # disable deselect/delete buttons
        self.actionDeselect.setEnabled(False)
        self.actionDelete.setEnabled(False)

        # select -> pan
        iface.actionPan().trigger()

    def onDelete(self):
        """Delete selected features.

        Ask user to confirm this action.
        """
        layer = self.getActiveLayer()
        if not layer:
            return

        count = layer.selectedFeatureCount()
        if count > 0:
            # ask if features should be really deleted (no undo avaialble)
            reply = QMessageBox.question(self, self.tr("Delete?"),
                                         self.tr("Do you want to delete {} selected features? "
                                                 "This operation cannot be reverted.").format(count),
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                # delete selected features from currently selected layer
                iface.messageBar().pushMessage(
                    self.tr("Info"),
                    self.tr("Updating attributes..."),
                    level=QgsMessageBar.INFO,
                    duration=1
                )
                layer.setReadOnly(False)
                iface.actionToggleEditing().trigger()
                iface.actionDeleteSelected().trigger()
                self.actionUpdateStatsPlot.trigger()
                iface.actionSaveActiveLayerEdits().trigger()
                iface.actionToggleEditing().trigger()
                layer.setReadOnly(True)
        else:
            # inform user - no features selected, nothing to be deleted
            iface.messageBar().pushMessage(self.tr("Info"), self.tr("No features selected. Nothing to be deleled."),
                                           level=QgsMessageBar.INFO, duration=3)
            # disable deselect/delete buttons
            self.actionDeselect.setEnabled(False)
            self.actionDelete.setEnabled(False)
            
    def onStorageFormat(self, idx):
        """Storage format changed.
        """
        # remember current storage format
        sender = 'safecast-{}-lastCurrentIndex'.format(self.sender().objectName())
        self._settings.setValue(sender, idx)

    def onAddOnlineMap(self):
        """Add online basemap to layer tree
        """
        idx = self.onlineMapsCombo.currentIndex()
        name, baseParams = self._onlineMaps[idx]
        datasource = baseParams + self._onlineMapsDefaultParams
        layer = QgsRasterLayer(datasource,
                               name,
                               'wms'
        )
        QgsMapLayerRegistry.instance().addMapLayer(layer, False)
        # force register layer in TOC as a last item
        QgsProject.instance().layerTreeRoot().insertLayer(-1, layer)
        # collapse layer
        iface.legendInterface().setLayerExpanded(layer, False)

    def getActiveLayer(self):
        """Get currently selected (active) layer.

        :return: layer instance
        """
        try:
            layer = iface.activeLayer()
            if not layer:
                raise SafecastError(self.tr("No layer loaded or selected"))
        except SafecastError as e:
            iface.messageBar().pushMessage(self.tr("Info"), self.tr("No active layer available."),
                                           level=QgsMessageBar.INFO, duration=3)
            return None

        return layer

    def _getLayerHelper(self, layer):
        """Get Safecast helper class from selected layer.

        :param: layer Safecast layer
        """
        if not layer:
            return None

        try:
            helper = self._layers[layer.id()]
        except:
            helper = None
            # iface.messageBar().pushMessage(self.tr("Warning"),
            #                                self.tr("Unable to retrieve Safecast data for selected layer"),
            #                                level=QgsMessageBar.WARNING, duration=5)
        return helper

    def updateStats(self, layer):
        """Update statistics for currently selected safecast layer.

        :param layer: current layer
        """
        # attach stats widget if doesn't exist
        is_safecast_layer = self._checkSafecastLayer(layer)
        self._initStats(is_safecast_layer)
        if not is_safecast_layer:
            return

        helper = self._getLayerHelper(layer)
        if not helper:
            return

        stats = helper.stats()
        data = [(self.tr("Measured points"), "{0:d}".format(stats['count']))]
        if stats['count'] <= 0:
            self._statsWidget.clear()
            return

        self.groupStats.setTitle(self.tr("Layer statistics - {}").format(layer.name()))
        self._statsWidget.setData(OrderedDict([
            (self.tr('Route information'), [
                (self.tr('average speed (km/h)'), '{0:.1f}'.format(stats['route']['speed'])),
                (self.tr('total monitoring time'), stats['route']['time'],
                ),
                (self.tr('total distance (km)'), '{0:.3f}'.format(stats['route']['distance'] / 1000)),
            ]),
            (self.tr('Radiation values'), [
                (self.tr('maximum dose rate (microSv/h)'), '{0:.3f}'.format(stats['radiation']['max'])),
                (self.tr('average dose rate (microSv/h)'), '{0:.3f}'.format(stats['radiation']['avg'])),
                (self.tr('total dose (microSv)'), '{0:.3f}'.format(stats['radiation']['total'])),
            ]),
        ]))

    def updatePlot(self, layer):
        """Update plot for currently selected safecast layer.

        :param layer: current layer
        """
        # attach plot widget if doesn't exist
        self._initPlot(self._checkSafecastLayer(layer) and not plotMsg)

        helper = self._getLayerHelper(layer)
        if not helper:
            return

        # update plot curve
        if self._plotVisible:
            groupTitle = self.tr("Layer plot - {}").format(layer.name())
            plotStyle = self.plotStyleCombo.currentIndex()
            self._plotWidget.update(helper, plotStyle)
        else:
            groupTitle = self.tr("Plot")
        self.groupPlot.setTitle(groupTitle)

    def onUpdatePlugin(self):
        """Update plugin widgets.
        """
        layer = iface.activeLayer()
        enabled = True if layer and self._checkSafecastLayer(layer) else False
        if enabled:
            iface.messageBar().pushMessage(
                self.tr("Info"),
                self.tr("Updating statistics for {}...".format(layer.name())),
                level=QgsMessageBar.INFO,
                duration=3
            )

        self.actionSave.setEnabled(enabled)
        self.actionSelect.setEnabled(enabled)
        self.actionDeselect.setEnabled(enabled)
        self.actionDelete.setEnabled(enabled)

        self.actionUpdateStatsPlot.trigger()

    def onUpdateStatsPlot(self):
        """Update stats & plot for currently selected safecast layer.
        """
        layer = iface.activeLayer()

        # layer loaded from project
        if not isinstance(layer, SafecastLayer) and self._checkSafecastLayer(layer):
            helper = SafecastLayerHelper(layer)
            helper.computeStats()
            self._layers[layer.id()] = helper

        self.updateStats(layer)
        self.updatePlot(layer)

    def _checkSafecastLayer(self, layer):
        """Check if current map layer is managable by Safecast plugin.
        """
        if not layer:
            return False

        if isinstance(layer, SafecastLayer):
            # map layer loaded by Safecast plugin
            return True

        try:
            filePath = layer.dataProvider().dataSourceUri().split('|')[0]
            ds = ogr.Open(filePath)
            layer = ds.GetLayerByName('safecast_metadata')
            is_safecast_layer = True if layer else False
            ds = None
        except:
            is_safecast_layer = None

        return is_safecast_layer
