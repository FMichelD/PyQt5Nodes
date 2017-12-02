# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from inspect import currentframe, getframeinfo

from PyQt5.QtCore import *

from PortType import *
from StyleCollection import *

##----------------------------------------------------------------------------
class ConnectionGeometry(object):
    def __init__(self):
        self._in = QPointF(0, 0)
        self._out = QPointF(0, 0)

        self._lineWidth = 3.0
        self._hovered = False

    #-------------------------------------------------------------------------
    def getEndPoint(self, portType):
        if(portType != PortType.No_One):
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)


        return self._out if(portType == PortType.Out) else self._in

    #-------------------------------------------------------------------------
    def setEndPoint(self, portType, point):
        if(portType == PortType.Out):
            self._out = point
        elif(portType == PortType.In):
            self._in = point

    #-------------------------------------------------------------------------
    def moveEndPoint(self, portType, offset):
        if(portType == PortType.Out):
            self._out += offset
        elif(portType == PortType.In):
            self._in += offset

    #-------------------------------------------------------------------------
    def boundingRect(self):
        points = self.pointsC1C2()

        basicRect = QRectF(self._out, self._in).normalized()

        c1c2Rect = QRectF(points[0], points[1]).normalized()

        connectionStyle = StyleCollection.connectionStyle()

        diam = connectionStyle.pointDiameter()

        commonRect = basicRect.united(c1c2Rect)

        cornerOffset = QPointF(diam, diam)

        commonRect.setTopLeft(commonRect.topLeft() - cornerOffset)
        commonRect.setBottomRight(commonRect.bottomRight() + 2 * cornerOffset)

        return commonRect

    #-------------------------------------------------------------------------
    def pointsC1C2(self):

        xDistance = self._in.x() - self._out.x()

        defaultOffset = 200

        minimum = min(defaultOffset, abs(xDistance))

        verticalOffset = 0

        ratio1 = 0.5

        if(xDistance <= 0):
            verticalOffset = -minimum
            ratio1 = 1.0

        # //double verticalOffset2 = verticalOffset;
        # //if (xDistance <= 0)
        # //verticalOffset2 = qMin(defaultOffset, std::abs(yDistance));
        # //auto sign = [](double d) { return d > 0.0 ? +1.0 : -1.0; };
        # //verticalOffset2 = 0.0;

        c1 = QPointF(self._out.x() + minimum*ratio1,
                    self._out.y() + verticalOffset)

        c2 = QPointF(self._in.x() - minimum*ratio1,
                    self._in.y() + verticalOffset)

        return (c1, c2)

    #-------------------------------------------------------------------------
    def source(self):
        return self._out

    #-------------------------------------------------------------------------
    def sink(self):
        return self._in

    #-------------------------------------------------------------------------
    def lineWidth(self):
        return _lineWidth

    #-------------------------------------------------------------------------
    def hovered(self):
        return self._hovered

    #-------------------------------------------------------------------------
    def setHovered(self,  hovered: bool):
        self._hovered = hovered
##----------------------------------------------------------------------------

