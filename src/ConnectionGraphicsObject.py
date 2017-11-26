# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
import inspect

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#from FlowScene import *

#from Connection import *
#from ConnectionGeometry import *
from ConnectionPainter import *
#from ConnectionState import *
#from ConnectionBlurEffect import *

from NodeConnectionInteraction import *
from PortType import *

##----------------------------------------------------------------------------
class ConnectionGraphicsObject(QGraphicsObject):

    def __init__(self, scene, connection):
        
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        #print('caller name:', calframe[1][3])
        
        super().__init__()

        self._scene = scene

        self._connection = connection
        
        self._scene.addItem(self)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.setAcceptHoverEvents(True)

        self.setZValue(-1.0)

    #-------------------------------------------------------------------------
    def __del__(self):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print("ConnectionGraphicsObject: __del__(self)")
#        print('caller name:', calframe[1][3])
#        print('on:', calframe[1][1])
#        print('')
#        
#        print("Remove ConnectionGraphics from scene")

        self._scene.removeItem(self)

    #-------------------------------------------------------------------------
    def connection(self):

        return self._connection

    #-------------------------------------------------------------------------
    def boundingRect(self):

        return self._connection.connectionGeometry().boundingRect()

    #-------------------------------------------------------------------------
    def shape(self):

        geom = self._connection.connectionGeometry()

        return ConnectionPainter.getPainterStroke(geom)

    #----------------------------------------------------ConnectionGraphicsObject.py---------------------
    def setGeometryChanged(self):

        self.prepareGeometryChange()

    #-------------------------------------------------------------------------
    def move(self):
        def moveEndPoint(portType):
            node = self._connection.getNode(portType)

            if(not node is None):

                nodeGraphics = node.nodeGraphicsObject()

                nodeGeom = node.nodeGeometry()

                scenePos = nodeGeom.portScenePosition(self._connection.getPortIndex(portType),
                            portType, nodeGraphics.sceneTransform())

                sceneTransform = self.sceneTransform()

                connectionPos = sceneTransform.inverted()[0].map(scenePos)

                self._connection.connectionGeometry().setEndPoint(portType,
                                                                connectionPos)

                self._connection.getConnectionGraphicsObject().setGeometryChanged()

                self._connection.getConnectionGraphicsObject().update()

        moveEndPoint(PortType.In)
        moveEndPoint(PortType.Out)

    #-------------------------------------------------------------------------
    def paint(self, painter, option, widget):

        painter.setClipRect(option.exposedRect)

        ConnectionPainter.paint(painter, self._connection)

    #-------------------------------------------------------------------------
    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)

    #-------------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        self.prepareGeometryChange()        
        view = QGraphicsView(event.widget())

        node = self._scene.locateNodeAt(event.scenePos(), self._scene, view.transform())

        state = self._connection.connectionState()

        state.interactWithNode(node)

        if(node):
#            print("nodeId: ", node.id())
            node.reactToPossibleConnection(state.requiredPort(), 
                                            self._connection.dataType(),
                                            event.scenePos())

        offset = event.pos() - event.lastPos()

        requiredPort = self._connection.requiredPort()

        if not(requiredPort is PortType.No_One):

            self._connection.connectionGeometry().moveEndPoint(requiredPort, offset)

        self.update()

        event.accept()

    #-------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):

        self.ungrabMouse()
        event.accept()

        node = self._scene.locateNodeAt(event.scenePos(), self._scene,
                                self._scene.views()[0].transform())

        interaction = NodeConnectionInteraction(node, self._connection, self._scene)

        if((not node is None) and interaction.tryConnect()):
            node.resetReactionToConnection()
        elif(self._connection.connectionState().requiresPort()):
            self._scene.removeItem(self)
            self._scene.deleteConnection(self._connection)

    #-------------------------------------------------------------------------
    def hoverEnterEvent(self, event):
        self._connection.connectionGeometry().setHovered(True)
        self.update()
        self._scene.connectionHovered.emit(self.connection(), event.screenPos())
        event.accept()      
        
    #-------------------------------------------------------------------------
    def hoverLeaveEvent(self, event):
        self._connection.connectionGeometry().setHovered(False)
        self.update()
        self._scene.connectionHoverLeft.emit(self.connection())
        event.accept()
        
    #-------------------------------------------------------------------------
    def addGraphicsEffect(self):

        effect = QGraphicsBlurEffect()

        effect.setBlurRadius(5)

        self.setGraphicsEffect(effect)

        # //auto effect = new QGraphicsDropShadowEffect;
        # //auto effect = new ConnectionBlurEffect(this);
        # //effect->setOffset(4, 4);
        # //effect->setColor(QColor(Qt::gray).darker(800));

##----------------------------------------------------------------------------
