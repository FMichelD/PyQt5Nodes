# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
import inspect

from PyQt5.QtGui import  *

from PyQt5Nodes.Node import *
from PyQt5Nodes.FlowScene import *
from PyQt5Nodes.NodeGraphicsObject import *
from PyQt5Nodes.NodeGeometry import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeState import *
from PyQt5Nodes.StyleCollection import *

##----------------------------------------------------------------------------
class NodePainter(object):
    
    def __init__(self):
        pass

    #-------------------------------------------------------------------------
    @staticmethod
    def paint(painter: QPainter, node, scene):

        geom = node.nodeGeometry()
        state = node.nodeState()
        graphicsObject = node.nodeGraphicsObject()

        geom.recalculateSize(painter.font())
        
        model = node.nodeDataModel()

        NodePainter.drawNodeRect(painter, geom, model, graphicsObject)        
        
        NodePainter.drawConnectionPoints(painter, geom, node, model, scene)

        NodePainter.drawFilledConnectionPoints(painter, geom, state, model)

        NodePainter.drawModelName(painter, geom, state, model)

        NodePainter.drawEntryLabels(painter, geom, state, model)

        NodePainter.drawResizeRect(painter, geom, model)

        NodePainter.drawValidationRect(painter, geom, model, graphicsObject)
    
        # call custom painter
        painterDelegate = model.painterDelegate()
        if(painterDelegate):
            painterDelegate.painter(painter, geom, model)

    #-------------------------------------------------------------------------      
    @staticmethod
    def drawNodeRect(painter: QPainter,
                        geom: NodeGeometry,
                        model: NodeDataModel, 
                        graphicsObject):

        nodeStyle = model.nodeStyle()

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
                
                connPolicy = model.portOutConnectionPolicy(i) == ConnectionPolicy.Many
                
                canConnect = ((not node.nodeState().getEntries(portType)[i]) or
                                (portType == PortType.Out and connPolicy) )

       
                if(node.nodeState().isReacting().value and 
                        canConnect and
                        portType == node.nodeState().reactingPortType()):
                    
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
                        r = (2.0 - dist/thres) if(dist < thres) else 1.0                        
                    else:
                        thres = 40.0
                        r = (dist/thres) if(dist < thres) else 1.0
                

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
            if(modelValidationState == NodeValidationState.ERROR):

                painter.setBrush(nodeStyle.ErrorColor)

            else:

                painter.setBrush(nodeStyle.WarningColor)

            radius = 3.0

            diam = nodeStyle.ConnectionPointDiameter

#            boundary = QRectF(-diam,
#                                -diam + geom.height() + geom.validationHeight(),
#                                2.0 * diam + geom.width(),
#                                2.0 * diam + geom.validationHeight())
                                

            boundary = QRectF(-diam,
                              geom.height() - geom.validationHeight(),
                                2.0 * diam + geom.width(),
                                2.0 * diam + geom.validationHeight())

            painter.drawRoundedRect(boundary, radius, radius)

            painter.setBrush(Qt.gray)

            # Drawing the validation message itself
            errorMsg = model.validationMessage()

            f = painter.font()

            metrics = QFontMetrics(f)

            rect = metrics.boundingRect(errorMsg)

#            position = QPointF((geom.width() - rect.width())/2.0, 
#                    geom.height() - (geom.validationHeight() - diam)/2.0)

            position = QPointF((geom.width() - rect.width())/2.0, 
                    (geom.height() - geom.validationHeight()/2.0) + rect.height())

            painter.setFont(f)
            painter.setPen(nodeStyle.FontColor)
            painter.drawText(position, errorMsg)

#-----------------------------------------------------------------------------
