# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from enum import Enum

from PyQt5Nodes.FlowScene import *

from PyQt5Nodes.Connection import *
from PyQt5Nodes.ConnectionGeometry import *
from PyQt5Nodes.ConnectionPainter import *
from PyQt5Nodes.ConnectionState import *
from PyQt5Nodes.ConnectionBlurEffect import *

from PyQt5Nodes.Node import *
from PyQt5Nodes.NodeGraphicsObject import *
from PyQt5Nodes.NodeConnectionInteraction import *

from PyQt5Nodes.PortType import *

##----------------------------------------------------------------------------
class ConnectionGraphicsObject(QGraphicsObject):
    def __init__(self, scene, connection):
        super().__init__()

        self.QGType = QGraphicsObject.UserType + 1

        self._scene = scene
        self._connection = connection

        self._scene.addItem(self)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.setAcceptHoverEvents(True)

#        self.addGraphicsEffect()

        self.setZValue(-1.0)

    #-------------------------------------------------------------------------
    def __del__(self):
        self._scene.removeItem(self)

    #-------------------------------------------------------------------------
    def connection(self):
        return self._connection

    #-------------------------------------------------------------------------
    #override
    def boundingRect(self):
        return self._connection.connectionGeometry().boundingRect()

    #-------------------------------------------------------------------------
    #override
    def shape(self):
        geom = self._connection.connectionGeometry()

        return ConnectionPainter.getPainterStroke(geom)

    #-------------------------------------------------------------------------
    def setGeometryChanged(self):
        self.prepareGeometryChange()

    #-------------------------------------------------------------------------
    def move(self):
        def moveEndPoint(portType):
            node = self._connection.getNode(portType)

            if(node):
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
    def lock(self,  locked: bool):
        self.setFlag(QGraphicsItem.ItemIsMovable, not locked)
        setFlag(QGraphicsItem.ItemIsFocusable, not locked)
        setFlag(QGraphicsItem.ItemIsSelectable, not locked)

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

        logging.debug("CGO.py verificar locateNodeAt na ln: 127")
        node = self._scene.locateNodeAt(event.scenePos(), self._scene, view.transform())

        state = self._connection.connectionState()

        state.interactWithNode(node)

        if(node):
            logging.debug("Node: {}".format(node.id()))
            node.reactToPossibleConnection(state.requiredPort(),
                                            self._connection.dataType(),
                                            event.scenePos())

        offset = event.pos() - event.lastPos()

        requiredPort = self._connection.requiredPort()

        if (requiredPort is not PortType.No_One):
            self._connection.connectionGeometry().moveEndPoint(requiredPort, offset)

        logging.debug("CGO.py verificar ln: 146")
        if(node):
            node.nodeGraphicsObject().update()

        self.update()

        event.accept()

    #-------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):

        self.ungrabMouse()
        event.accept()

        logging.debug("CGO.py verificar locateNodeAt na ln: 161")
        node = self._scene.locateNodeAt(event.scenePos(), self._scene,
                                self._scene.views()[0].transform())

        interaction = NodeConnectionInteraction(node, self._connection, self._scene)

        if(node and interaction.tryConnect()):
            node.resetReactionToConnection()
        elif(self._connection.connectionState().requiresPort()):
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

    #-------------------------------------------------------------------------
    #override
    def type(self):
        return self.QGType
##----------------------------------------------------------------------------
