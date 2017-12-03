# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5Nodes.ConnectionGeometry import *
from PyQt5Nodes.ConnectionState import *
from PyQt5Nodes.Connection import *
from PyQt5Nodes.ConnectionGraphicsObject import *

from PyQt5Nodes.NodeData import *
from PyQt5Nodes.StyleCollection import *



##----------------------------------------------------------------------------
class ConnectionPainter(object):

    def __init__(self):
        pass

    #-------------------------------------------------------------------------
    @staticmethod
    def cubicPath(geom):
        source = QPointF(geom.source())
        sink = QPointF(geom.sink())

        c1c2 = geom.pointsC1C2()

        cubic = QPainterPath(source)
        cubic.cubicTo(c1c2[0], c1c2[1], sink)

        return cubic

    #-------------------------------------------------------------------------
    @staticmethod
    def getPainterStroke(geom):

        cubic = ConnectionPainter.cubicPath(geom)

        source = geom.source()
        result = QPainterPath(source)

        segments = 20

        for i in range(0, segments):
            ratio = float(i + 1) / segments
            result.lineTo(cubic.pointAtPercent(ratio))

        stroker = QPainterPathStroker()
        stroker.setWidth(10.0)

        return stroker.createStroke(result)

    #-------------------------------------------------------------------------
    @staticmethod
    def paint(painter, connection):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\ncaller name:', calframe[1][3])
#        print('on:', calframe[1][1])

        connectionStyle = StyleCollection.connectionStyle()

        normalColor = connectionStyle.normalColor()
        hoverColor = connectionStyle.hoveredColor()
        selectedColor = connectionStyle.selectedColor()

        dataType = connection.dataType()

        if(connectionStyle.useDataDefinedColors()):
            normalColor = connectionStyle.normalColor(dataType.id)
            hoverColor = normalColor.lighter(200)
            selectedColor = normalColor.darker(200)

        geom = connection.connectionGeometry()
        state = connection.connectionState()

        lineWidth = connectionStyle.lineWidth()
        pointDiameter = connectionStyle.pointDiameter()

        cubic = ConnectionPainter.cubicPath(geom)

        hovered = geom.hovered()

        graphicsObject = connection.getConnectionGraphicsObject()

        selected = graphicsObject.isSelected()

        if(hovered or selected):
            p = QPen()

            p.setWidth(2 * lineWidth)

            p.setColor(connectionStyle.selectedHaloColor() if selected else
                                                                    hoverColor)

            painter.setPen(p)
            painter.setBrush(Qt.NoBrush)

            # Cubic spline
            painter.drawPath(cubic)


        p = QPen()
        p.setWidth(lineWidth)

        if(selected):
            p.setColor(selectedColor)
        else:
            p.setColor(normalColor)

        if(state.requiresPort()):
            p.setWidth(connectionStyle.constructionLineWidth())
            p.setColor(connectionStyle.constructionColor())
            p.setStyle(Qt.DashLine)

        painter.setPen(p)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(cubic)

        source = geom.source()
        sink = geom.sink()

        painter.setPen(connectionStyle.constructionColor())
        painter.setBrush(connectionStyle.constructionColor())
        pointRadius = pointDiameter / 2.0
        painter.drawEllipse(source,  pointRadius, pointRadius)
        painter.drawEllipse(sink, pointRadius, pointRadius)

##----------------------------------------------------------------------------
