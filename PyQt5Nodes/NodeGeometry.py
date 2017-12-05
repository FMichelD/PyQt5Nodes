# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from typing import *
import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5Nodes.PortType import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.Node import *
from PyQt5Nodes.StyleCollection import *

#-----------------------------------------------------------------------------
class NodeGeometry(object):

    def __init__(self, dataModel: NodeDataModel):

        self._width = 100
        
        self._height = 150
        
        self._inputPortWidth = 70

        self._outputPortWidth = 70

        self._entryHeight = 20

        self._entryWidth  = 50

        self._spacing = 20

        self._hovered = False

        self._nSources = dataModel.nPorts(PortType.Out)

        self._nSinks = dataModel.nPorts(PortType.In)

        self._dragginPos = QPointF(-1000,-1000)

        self._dataModel = dataModel

        self._fontMetrics = QFontMetrics(QFont())

        self._boldFontMetrics = QFontMetrics(QFont())


        f = QFont()
        f.setBold(True)
        self._boldFontMetrics = QFontMetrics(f)

    #-------------------------------------------------------------------------
    def height(self) -> int:

        return self._height

    #-------------------------------------------------------------------------
    def setHeight(self, h: int):

        self._height = h

    #-------------------------------------------------------------------------
    def width(self) -> int:

        return self._width

    #-------------------------------------------------------------------------
    def  setWidth(self, w: int):
        
        self._width = w

    #-------------------------------------------------------------------------
    def entryHeight(self) -> int:

        return self._entryHeight

    #-------------------------------------------------------------------------
    def setEntryHeight(self, h: int):

        self._entryHeight = h

    #-------------------------------------------------------------------------
    def entryWidth(self) -> int:

        return self._entryWidth

    #-------------------------------------------------------------------------
    def setEntryWidth(self, w: int):

        self._entryWidth = w

    #-------------------------------------------------------------------------
    def spacing(self) -> int:

        return self._spacing

    #-------------------------------------------------------------------------
    def setSpacing(self, s: int):

        self._spacing = s

    #-------------------------------------------------------------------------
    def hovered(self) -> bool:

        return self._hovered

    #-------------------------------------------------------------------------
    def setHovered(self, h: bool):

        self._hovered = h

    #-------------------------------------------------------------------------
    def nSources(self) -> int:

        return self._nSources

    #-------------------------------------------------------------------------
    def nSinks(self) -> int:

        return self._nSinks

    #-------------------------------------------------------------------------
    def draggingPos(self) -> QPointF:

        return self._dragginPos    

    #-------------------------------------------------------------------------
    def setDraggingPosition(self, pos: QPointF):

        self._dragginPos = pos

    #-------------------------------------------------------------------------
    def entryBoundingRect(self) -> QRectF:

        addon = 0.0

        return QRectF(0 - addon,
                        0 - addon,
                        self._entryWidth + 2*addon,
                        self._entryHeight + 2*addon)

#-----------------------------------------------------------------------------
    def boundingRect(self) -> QRectF:
        
        nodeStyle = StyleCollection.nodeStyle()

        addon = 2 * nodeStyle.ConnectionPointDiameter

        return QRectF(0 - addon, 0 - addon,
                      self._width + 2*addon, self._height + 2*addon)

#-----------------------------------------------------------------------------
    def recalculateSize(self, font=None):

        if(font == None):

            self._entryHeight = self._fontMetrics.height()

            maxNumOffEntries = max(self._nSinks, self._nSources)

            step = self._entryHeight + self._spacing

            self._height = step * maxNumOffEntries       
        
            w = self._dataModel.embeddedWidget()

            if(w):
                self._height = max(self._height, w.height())

            self._height += (self.captionHeight())

            self._inputPortWidth = self.portWidth(PortType.In) 

            self._outputPortWidth = self.portWidth(PortType.Out)

            self._width = self._inputPortWidth +\
                            self._outputPortWidth +\
                            2 * self._spacing

            if(not w is None):
                self._width += w.width()

            self._width =  max(self._width, self.captionWidth())

            if(self._dataModel.validationState() != NodeValidationState.VALID):
                self._width = max(self._width, self.validationWidth())

                self._height += 2.0 * self.validationHeight()
                
        elif(isinstance(font, QFont)):

            fontMetrics = QFontMetrics(font)

            boldFont = font

            boldFont.setBold(True)

            boldFontMetrics = QFontMetrics(boldFont)

            if(self._boldFontMetrics != boldFontMetrics):
                self._fontMetrics = fontMetrics
                self._boldFontMetrics = boldFontMetrics

                self.recalculateSize()

#-----------------------------------------------------------------------------
    def portScenePosition(self, index: int, portType: PortType,
                            t: QTransform=QTransform()) -> QPointF: 

        nodeStyle = StyleCollection.nodeStyle()

        step = self._entryHeight + self._spacing

        result = QPointF()

        totalHeight = 0.0

        totalHeight += self.captionHeight()

        totalHeight += step * index

        # TODO: why?
        totalHeight += step / 2.0

        if(portType == PortType.Out):
            
            x = self._width + nodeStyle.ConnectionPointDiameter

            result = QPointF(x,  totalHeight)

        elif(portType == PortType.In):

            x = 0.0 - nodeStyle.ConnectionPointDiameter

            result = QPointF(x, totalHeight)

        return t.map(result)


#-----------------------------------------------------------------------------
    def checkHitScenePoint(self, portType: PortType, scenePoint: QPointF,
                            sceneTransformation: QTransform=QTransform()) -> PortIndex:

        nodeStyle = StyleCollection.nodeStyle()

        result = INVALID

        if(portType == PortType.No_One):
            return result

        tolerance = 2.0 * nodeStyle.ConnectionPointDiameter

        nItems = self._dataModel.nPorts(portType)

        for i in range(0, nItems):

            pp = self.portScenePosition(i, portType, sceneTransformation)

            p = pp - scenePoint

            distance = math.sqrt(QPointF.dotProduct(p, p))

            if(distance < tolerance):
                result = PortIndex(i)            
                break

        return result

    #-------------------------------------------------------------------------
    def resizeRect(self):

        rectSize = 3

        return QRect(self._width - rectSize,
                    self._height - rectSize,
                    rectSize, rectSize)

#-----------------------------------------------------------------------------
    def widgetPosition(self) -> QPointF:

        w = self._dataModel.embeddedWidget()

        if(w):
            if(self._dataModel.validationState() != NodeValidationState.VALID):
                return  QPointF(self._spacing + self.portWidth(PortType.In),
                                (self.captionHeight() + self._height -
                                self.validationHeight() - self._spacing - 
                                w.height()) / 2.0)
                                
            return QPointF(self._spacing + self.portWidth(PortType.In), 
                            (self.captionHeight() + self._height - w.height()) / 2.0)

        return QPointF()         

#-----------------------------------------------------------------------------
    def captionHeight(self) -> int:

        if(not self._dataModel.captionVisible()):
            return 0

        name = self._dataModel.caption()

        return self._boldFontMetrics.boundingRect(name).height()

#-----------------------------------------------------------------------------
    def captionWidth(self) -> int:

        if(not self._dataModel.captionVisible()):
            return 0

        name = self._dataModel.caption()
        
        return self._boldFontMetrics.boundingRect(name).width()

#-----------------------------------------------------------------------------
    def validationHeight(self) -> int:
        
        msg = self._dataModel.validationMessage()

        return self._boldFontMetrics.boundingRect(msg).height()

#-----------------------------------------------------------------------------
    def validationWidth(self) -> int:

        msg = self._dataModel.validationMessage()

        return self._boldFontMetrics.boundingRect(msg).width()
    
#-----------------------------------------------------------------------------
    def calculateNodePositionBetweenPorts(self, targetPortIndex: PortIndex,
                        targetPort: PortType, targetNode,
                        sourcePortIndex: PortIndex, sourceNode,
                        sourcePort: PortType, newNode) -> QPointF:

        # //Calculating the nodes position in the scene. It'll be positioned half way between the two ports that it "connects". 
        # //The first line calculates the halfway point between the ports (node position + port position on the node for both nodes averaged).
        # //The second line offsets this coordinate with the size of the new node, so that the new nodes center falls on the originally
        # //calculated coordinate, instead of it's upper left corner
        converterNodePos = (sourceNode.nodeGraphicsObject().pos() + 
    sourceNode.nodeGeometry().portScenePosition(sourcePortIndex, sourcePort) +
    targetNode.nodeGraphicsObject().pos() +
    targetNode.nodeGeometry().portScenePosition(targetPortIndex, targetPort)) / 2.0

        converterNodePos.setX(converterNodePos.x() - newNode.nodeGeometry().width() / 2.0)

        converterNodePos.setY(converterNodePos.y() - newNode.nodeGeometry.height() / 2.0)

        return converterNodePos

#-----------------------------------------------------------------------------
    def portWidth(self, portType: PortType) -> int:

        width = 0

        for i in range(0, self._dataModel.nPorts(portType)):

            if(self._dataModel.portCaptionVisible(portType, i)):

                name = self._dataModel.portCaption(portType, i)
        
            else:

                name = self._dataModel.dataType(portType, i).name

            width = max(self._fontMetrics.width(name), width)

        return width

#-----------------------------------------------------------------------------

