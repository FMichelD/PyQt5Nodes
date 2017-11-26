# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
import inspect

from PyQt5.QtGui import  *

from Node import *
from FlowScene import *
from NodeGraphicsObject import *
from NodeGeometry import *
from NodeDataModel import *
from NodeState import *
from StyleCollection import *

##----------------------------------------------------------------------------
class NodePainter(object):
    
    def __init__(self):
        pass

    #-------------------------------------------------------------------------
    @staticmethod
    def paint(painter: QPainter, node, scene):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\nNodePainter.py: paint(...)')
#        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))
        
        geom = node.nodeGeometry()

        state = node.nodeState()

        graphicsObject = node.nodeGraphicsObject()

        geom.recalculateSize(painter.font())

        NodePainter.drawNodeRect(painter, geom, graphicsObject)

        model = node.nodeDataModel()
        
        NodePainter.drawConnectionPoints(painter, geom, node, model, scene)

        NodePainter.drawFilledConnectionPoints(painter, geom, state, model)

        NodePainter.drawModelName(painter, geom, state, model)

        NodePainter.drawEntryLabels(painter, geom, state, model)

        NodePainter.drawResizeRect(painter, geom, model)

        NodePainter.drawValidationRect(painter, geom, model, graphicsObject)

    #-------------------------------------------------------------------------      
    @staticmethod
    def drawNodeRect(painter: QPainter, geom: NodeGeometry,
                        graphicsObject: QGraphicsItem):

        nodeStyle = StyleCollection.nodeStyle()

        if(graphicsObject.isSelected()):

            color = nodeStyle.SelectedBoundaryColor

        else:

            color = nodeStyle.NormalBoundaryColor


        if(geom.hovered()):

            p = QPen(color, nodeStyle.HoveredPenWidth)

            painter.setPen(p)

        else:

            p = QPen(color, nodeStyle.PenWidth)

            painter.setPen(p)

        gradient = QLinearGradient(QPointF(0.0, 0.0), QPointF(2.0, geom.height()))

        gradient.setColorAt(0.0, nodeStyle.GradientColor0)
        gradient.setColorAt(0.03, nodeStyle.GradientColor1)
        gradient.setColorAt(0.97, nodeStyle.GradientColor2)
        gradient.setColorAt(1.0, nodeStyle.GradientColor3)

        painter.setBrush(gradient)

        diam = nodeStyle.ConnectionPointDiameter

        boundary = QRectF(-diam, -diam, 2.0*diam + geom.width(), 
                            2.0*diam + geom.height())

        radius = 3.0

        painter.drawRoundedRect(boundary, radius, radius)

    #-------------------------------------------------------------------------
    @staticmethod
    def drawConnectionPoints(painter, geom, node, model, scene):
        
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('\nNodePainter.py: drawConnectionPoints(...)')
        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))
        
        nodeStyle = StyleCollection.nodeStyle()

        connectionStyle = StyleCollection.connectionStyle()

        diameter = nodeStyle.ConnectionPointDiameter

        reducedDiameter = diameter * 0.6

        #inner function
        def drawPoints(portType: PortType):

            n = len(node.nodeState().getEntries(portType))

            for i in range(0, n):

                p = geom.portScenePosition(i, portType)

                dataType = model.dataType(portType, i)

                r = 1.0
                
                print('\n***** NodeId:{} isReacting: {}*****\n'.format(node.id(),  node.nodeState().isReacting().value))
                if(node.nodeState().isReacting().value == True):
                    
#                    print("state.getEntries(portType)[i]: ", state.getEntries(portType)[i])
#                    print("portType: ", portType)
                    
                    if( ( not(bool(node.nodeState().getEntries(portType)[i])) or portType == PortType.Out) and portType == node.nodeState().reactingPortType()):

                        diff = geom.draggingPos() - p

                        dist = math.sqrt(QPointF.dotProduct(diff, diff))

                        typeConvertable = False

                        if(portType == PortType.In):

                            typeConvertable = scene.registry().getTypeConverter(
                                        node.nodeState().reactingDataType().id, dataType.id) != None
                        else:

                            typeConvertable = scene.registry().getTypeConverter(
                                        dataType.id, node.nodeState().reactingDataType().id) != None


                        if(node.nodeState().reactingDataType().id == dataType.id or typeConvertable):

                            thres = 40.0

                            if(dist < thres):

                                r = (2.0 - dist/thres)

                            else:

                                r = 1.0

                if(connectionStyle.useDataDefinedColors()):

                    painter.setBrush(connectionStyle.normalColor(dataType.id))

                else:

                    painter.setBrush(nodeStyle.ConnectionPointColor)

                painter.drawEllipse(p, reducedDiameter * r, reducedDiameter * r)

        drawPoints(PortType.In)
        drawPoints(PortType.Out)

    #-------------------------------------------------------------------------
    @staticmethod
    def drawFilledConnectionPoints(painter, geom, state, model):

        nodeStyle = StyleCollection.nodeStyle()

        connectionStyle = StyleCollection.connectionStyle()

        diameter = nodeStyle.ConnectionPointDiameter

        #inner function
        def drawPoints(portType: PortType):

            n = len(state.getEntries(portType))

            for i in range(0, n):

                p = geom.portScenePosition(i, portType)

                if(state.getEntries(portType)[i]):

                    dataType = model.dataType(portType, i)

                    if(connectionStyle.useDataDefinedColors()):

                        c = connectionStyle.normalColor(dataType.id)

                        painter.setPen(c)
                        painter.setBrush(c)

                    else:

                        painter.setPen(nodeStyle.FilledConnectionPointColor)
                        painter.setBrush(nodeStyle.FilledConnectionPointColor)

                    painter.drawEllipse(p, diameter * 0.4, diameter * 0.4)

        drawPoints(PortType.In)
        drawPoints(PortType.Out)

    #-------------------------------------------------------------------------
    @staticmethod
    def drawModelName(painter, geom, state, model):

        nodeStyle = StyleCollection.nodeStyle()

        if(not model.captionVisible()):

            return

        name = model.caption()

        f = painter.font()

        f.setBold(True)

        metrics = QFontMetrics(f)

        rect = metrics.boundingRect(name)

        position = QPointF((geom.width() - rect.width())/2.0, 
                            (geom.spacing() + geom.entryHeight())/3.0)

        painter.setFont(f)
        painter.setPen(nodeStyle.FontColor)
        painter.drawText(position, name)

        f.setBold(False)
        painter.setFont(f)

    #-------------------------------------------------------------------------
    @staticmethod
    def drawEntryLabels(painter, geom, state, model):

        metrics = painter.fontMetrics()
        
        #inner function
        def drawPoints(portType: PortType):
            
            p = None
            s = ""

            nodeStyle = StyleCollection.nodeStyle()

            entries = state.getEntries(portType)

            n = len(entries)

            for i in range(0, n):

                p = geom.portScenePosition(i, portType)

                if(not entries[i]):
                    painter.setPen(nodeStyle.FontColorFaded)
                else:
                    painter.setPen(nodeStyle.FontColor)

                if(model.portCaptionVisible(portType, i)):
                    s = model.portCaption(portType, i)
                else:
                    s = model.dataType(portType, i).name

                rect = metrics.boundingRect(s)

                p.setY(p.y() + rect.height() / 4.0)

                if(portType == PortType.In):
                    p.setX(5.0)
                elif(portType == PortType.Out):
                    p.setX(geom.width() - 5.0 -rect.width())
                else:
                    pass

                painter.drawText(p, s)

        drawPoints(PortType.In)
        drawPoints(PortType.Out)

    #-------------------------------------------------------------------------
    @staticmethod
    def drawResizeRect(painter, geom, model):

        if(model.resizable()):

            painter.setBrush(Qt.gray)

            painter.drawEllipse(geom.resizeRect())

    #-------------------------------------------------------------------------
    @staticmethod
    def drawValidationRect(painter, geom, model, graphicsObject):

        modelValidationState = model.validationState()

        if(modelValidationState != NodeValidationState.VALID):

            nodeStyle = StyleCollection.nodeStyle()

            if(graphicsObject.isSelected()):

                color = nodeStyle.SelectedBoundaryColor

            else:

                color = nodeStyle.NormalBoundaryColor

            if(geom.hovered()):

                p = QPen(color, nodeStyle.HoveredPenWidth)

                painter.setPen(p)

            else:

                p = QPen(color, nodeStyle.PenWidth)

                painter.setPen(p)

            # Drawing the validation message background
            if(modelValidationState == NodeValidationState.Error):

                painter.setBrush(nodeStyle.ErrorColor)

            else:

                painter.setBrush(nodeStyle.WarningColor)

            radius = 3.0

            diam = nodeStyle.ConnectionPointDiameter

            boundary = QRectF(-diam,
                                -diam + geom.height() - geom.validationHeigth(),
                                2.0*diam + geom.width(),
                                2.0*diam + geom.validationHeigth())

            painter.drawRoundedRect(boundary, radius, radius)

            painter.setBrush(Qt.gray)

            # Drawing the validation message itself
            #print("mensage erro nodepainter line:363")
            errorMsg = model.validationMessage()

            f = painter.font()

            metrics = QFontMetrics(f)

            rect = metrics.boundingRect(errorMsg)

            position = QPointF((geom.width() - rect.width())/2.0, 
                    geom.height() - (geom.validationHeigth() - diam)/2.0)

            painter.setFont(f)
            painter.setPen(nodeStyle.FontColor)
            painter.drawText(position, errorMsg)

#-----------------------------------------------------------------------------
