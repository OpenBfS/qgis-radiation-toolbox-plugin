"""
/***************************************************************************
                             A QGIS Safecast Plugin
                             ----------------------
        begin                : 2016-05-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by OpenGeoLabs s.r.o.
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

from PyQt4 import Qt
try:
    import qwt as Qwt
    hasQwt5 = False
except:
    import PyQt4.Qwt5 as Qwt
    hasQwt5 = True

class SafecastAxis(Qwt.QwtPlotItem):
    """Supports a coordinate system similar to 
    http://en.wikipedia.org/wiki/Image:Cartesian-coordinate-system.svg

    Based on http://pyqwt.sourceforge.net/examples/CartesianDemo.py.html
    """

    def __init__(self, masterAxis, slaveAxis):
        """Valid input values for masterAxis and slaveAxis are QwtPlot.yLeft,
        QwtPlot.yRight, QwtPlot.xBottom, and QwtPlot.xTop. When masterAxis is
        an x-axis, slaveAxis must be an y-axis; and vice versa.
        """
        Qwt.QwtPlotItem.__init__(self)
        self.__axis = masterAxis
        if masterAxis in (Qwt.QwtPlot.yLeft, Qwt.QwtPlot.yRight):
            self.setAxes(slaveAxis, masterAxis)
        else:
            self.setAxes(masterAxis, slaveAxis)
        self.scaleDraw = Qwt.QwtScaleDraw()
        self.scaleDraw.setAlignment((Qwt.QwtScaleDraw.LeftScale,
                                     Qwt.QwtScaleDraw.RightScale,
                                     Qwt.QwtScaleDraw.BottomScale,
                                     Qwt.QwtScaleDraw.TopScale)[masterAxis])

    def draw(self, painter, xMap, yMap, rect):
        """Draw an axis on the plot canvas
        """
        if self.__axis in (Qwt.QwtPlot.yLeft, Qwt.QwtPlot.yRight):
            if hasQwt5:
                self.scaleDraw.move(round(xMap.xTransform(0.0)), yMap.p2())
            else:
                self.scaleDraw.move(round(xMap.transform(0.0)), yMap.p2())
            self.scaleDraw.setLength(yMap.p1()-yMap.p2())
        elif self.__axis in (Qwt.QwtPlot.xBottom, Qwt.QwtPlot.xTop):
            if hasQwt5:
                self.scaleDraw.move(xMap.p1(), round(yMap.xTransform(0.0)))
            else:
                self.scaleDraw.move(xMap.p1(), round(yMap.transform(0.0)))
            self.scaleDraw.setLength(xMap.p2()-xMap.p1())
        self.scaleDraw.setScaleDiv(self.plot().axisScaleDiv(self.__axis))
        self.scaleDraw.draw(painter, self.plot().palette())


class SafecastPlot(Qwt.QwtPlot):
    """Creates a coordinate system similar system 
    http://en.wikipedia.org/wiki/Image:Cartesian-coordinate-system.svg

    Based on  http://pyqwt.sourceforge.net/examples/CartesianDemo.py.html
    """
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        # create a plot with a white canvas
        self.setCanvasBackground(Qt.Qt.white)

        # set plot layout
        if hasQwt5:
            self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)
        # attach a grid
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(Qt.QPen(Qt.Qt.black, 0, Qt.Qt.DotLine))

        # attach a x-axis
        xaxis = SafecastAxis(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft)
        xaxis.attach(self)
        if hasQwt5:
            self.setAxisTitle(Qwt.QwtPlot.xBottom, self.tr("Local Time"))
        else:
            self.setAxisTitle(Qwt.QwtPlot.xBottom, self.tr("Local Time"))
        # attach a y-axis
        yaxis = SafecastAxis(Qwt.QwtPlot.yLeft, Qwt.QwtPlot.xBottom)
        yaxis.attach(self)
        if hasQwt5:
            self.setAxisTitle(Qwt.QwtPlot.yLeft, self.tr("ADER [microSv/h]"))
        else:
            self.setAxisTitle(Qwt.QwtPlot.yLeft, self.tr("ADER [microSv/h]"))

    def update(self, layer, style):
        """Update plot for given Safecast layer.

        :param layer: Safecast layer
        """
        def time2float(value):
            h, m, s = map(float, value.split(':'))
            return h + m / 60. + s / 3600.
            
        # collect plot coordinates
        x, y = layer.plot_data()
            
        # clear plot first
        if hasQwt5:
            self.clear()
        else:
            self.detachItems([Qwt.QwtPlotItem.Rtti_PlotItem], True)

        # attach a curve
        curve = Qwt.QwtPlotCurve('ader_microSvh')
        curve.attach(self)

        if style == 0: # lines
            curve.setPen(Qt.QPen(Qt.Qt.blue, 0))
        else:          # points
            curve.setStyle(Qwt.QwtPlotCurve.NoCurve)
            curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
                                          Qt.QBrush(Qt.Qt.blue),
                                          Qt.QPen(Qt.Qt.blue),
                                          Qt.QSize(5, 5)))

        curve.setData(x, y)

        self.replot()
