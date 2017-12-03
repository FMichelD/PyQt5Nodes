# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import sys
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5Nodes.FlowScene import *
from PyQt5Nodes.NodeGeometry import *
from PyQt5Nodes.NodeState import *
from PyQt5Nodes.StyleCollection import *
from PyQt5Nodes.NodePainter import *
from PyQt5Nodes.NodeConnectionInteraction import *

##----------------------------------------------------------------------------
class NodeGraphicsObject(QGraphicsObject):

    def __init__(self, scene, node):
        super(NodeGraphicsObject,  self).__init__()

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print("\n NodeGraphicsObject.py: __init__(...)")
        print('caller name:', calframe[1][3])
        print('on:', calframe[1][1])

        self._scene = scene
        self._locked = False

        self._node = node
        self._nodeOriginal = node

        self._proxyWidget = None

        self._scene.addItem(self)

        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        self.setAcceptedMouseButtons(Qt.AllButtons)

        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(4.0, 4.0)
        effect.setBlurRadius(20)
        effect.setColor(self._node.nodeStyle().ShadowColor)
        self.setGraphicsEffect(effect)

        self.setOpacity(self._node.nodeStyle().Opacity)

        self.setAcceptHoverEvents(True)
        self.setZValue(0)
        self.embedQWidget()

        self.xChanged.connect(lambda: self._scene.moveNode(self._node,  self.pos()))
        self.yChanged.connect(lambda: self._scene.moveNode(self._node,  self.pos()))

    #-------------------------------------------------------------------------
    def __del__(self):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('caller name:', calframe[1][3])
#        print('on:', calframe[1][1])

        self._scene.removeItem(self)

    #-------------------------------------------------------------------------
    def node(self):
        return self._node

    #-------------------------------------------------------------------------
    def embedQWidget(self):

        geom = self._node.nodeGeometry()

        w = self._node.nodeDataModel().embeddedWidget()

        if(not w is None):
            self._proxyWidget = QGraphicsProxyWidget(self)

            self._proxyWidget.setWidget(w)

            self._proxyWidget.setPreferredWidth(5)

            geom.recalculateSize()

            self._proxyWidget.setPos(geom.widgetPosition())

            update()

            self._proxyWidget.setOpacity(1.0)

            self._proxyWidget.setFlag(QGraphicsItem.ItemIgnoreParentOpacity)

    #-------------------------------------------------------------------------
    def boundingRect(self) -> QRectF:
        return self._node.nodeGeometry().boundingRect()

    #-------------------------------------------------------------------------
    def setGeometryChanged(self):
        self.prepareGeometryChange()

    #-------------------------------------------------------------------------
    def moveConnections(self):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        #print('caller name:', calframe[1][3])
#        #print('on:', calframe[1][4])

        nodeState = self._node.nodeState()
#        #print(self._node.nodeState()._outConnections)

        def moveConnection(portType,  node):

            connectionsEntries = nodeState.getEntries(portType)

            #check for any connectionsEntrie empty
            if(any(d for d in connectionsEntries)):
                connections = [d for d in connectionsEntries if(d)]
                for connection in connections:
                    for id, con in connection.items():
                         con.getConnectionGraphicsObject().move()

        moveConnection(PortType.In,  self._node)
        moveConnection(PortType.Out,  self._node)

    #-------------------------------------------------------------------------
    def lock(self,  locked: bool):
        self._locked = locked

        self.setFlag(QGraphicsItem.ItemIsMovable, not(locked))
        self.setFlag(QGraphicsItem.ItemIsFocusable, not(locked))
        self.setFlag(QGraphicsItem.ItemIsSelectable, not(locked))

    #-------------------------------------------------------------------------
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
                widget: QWidget):

#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\nNodeGraphicsObject.py: paint(...)')
#        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))

        painter.setClipRect(option.exposedRect)

        NodePainter.paint(painter, self._node, self._scene)

    #-------------------------------------------------------------------------
    def itemChange(self, change, value: QVariant) -> QVariant:

        if(change == self.ItemPositionChange and bool(self.scene())):
            self.moveConnections()

        return QGraphicsItem.itemChange(self,  change, value)

    #-------------------------------------------------------------------------
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):

        if(self._locked):
            return

        # // deselect all other items after this one is selected
        if(not self.isSelected() and not(event.modifiers() == Qt.ControlModifier)):
            self._scene.clearSelection()

        # Inner function -----------------------------------------------------
        def clickPort(portToCheck):

            nodeGeometry = self._node.nodeGeometry()

            # TODO not pass sceneTransform
            portIndex = nodeGeometry.checkHitScenePoint(portToCheck,
                                                        event.scenePos(),
                                                        self.sceneTransform())

            if(portIndex != INVALID):
                nodeState = self._node.nodeState()
                
                #dict(QUuid, Connection)
                connections = nodeState.connections(portToCheck, portIndex)

                if(portToCheck == PortType.In):
                    print("Node: {}".format(self._node.id()))
#                    connections = self._node.nodeState().connections(portToCheck, portIndex)
                    connections = self._node.nodeState().getEntries(portToCheck)[portIndex]
                    
                # start dragging existing connection
#                print(connections)
#                if(connections):
#                    print(connections)
                    
                if(connections and portToCheck == PortType.In):
                    k = next(iter(connections))
#                    #print("k: ", k)
                    conn = connections[k]

                    interaction = NodeConnectionInteraction(self._node, conn,  self._scene)

                    interaction.disconnect(portToCheck)

                # initialize new Connection
                else:
                    outPolicy = self._node.nodeDataModel().portOutConnectionPolicy(portIndex)
                    if(connections and portToCheck == PortType.Out and
                            outPolicy == NodeDataModel.ConnectionPolicy.One):
                        self._scene.deleteConnection(connections[k])
                        
                    connection = self._scene.createConnection(portToCheck,
                                                                self._node,
                                                                portIndex)
                    
                    print(self._node.id())
                    self._node.nodeState().setConnection(portToCheck,
                                                            portIndex,
                                                            connection)
                
#                    #print("GrabMouse: ",  connection.getConnectionGraphicsObject())
                    connection.getConnectionGraphicsObject().grabMouse()
        # end inner function -------------------------------------------------

        clickPort(PortType.In)
        clickPort(PortType.Out)

        pos = event.pos()
        geom = self._node.nodeGeometry()
        state = self._node.nodeState()

        if(geom.resizeRect().contains(QPoint(pos.x(), pos.y()))):
            state.setResizing(True)

        if (self._node.nodeDataModel().resizable() and
          geom.resizeRect().contains(QPoint(pos.x(),
                                            pos.y()))):
            state.setResizing(true);

    #-------------------------------------------------------------------------
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        geom = self._node.nodeGeometry()

        state = self._node.nodeState()

        if(state.resizing()):
            diff = event.pos() - event.lastPos()

            w = self._node.nodeDataModel().embeddedWidget()

            if(w != 0):
                self.prepareGeometryChange()

                oldSize = w.size()

                oldSize  += QSize(diff.x(), diff.y())

                w.setFixedSize(oldSize)

                self._proxyWidget.setMinimunSize(oldSize)
                self._proxyWidget.setMaxinumSize(oldSize)
                self._proxyWidget.setPos(geom.widgetPosition())

                geom.recalculateSize()

                self.update()

                moveConnections();

                event.accept()

        else:
            QGraphicsObject.mouseMoveEvent(self, event)

            if(event.lastPos() != event.pos()):
                pass

                self.moveConnections()

            event.ignore()

        r = self.scene().sceneRect()

        r = r.united(self.mapToScene(self.boundingRect()).boundingRect())

        self.scene().setSceneRect(r)

    #-------------------------------------------------------------------------
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):

        state = self._node.nodeState()

        state.setResizing(False)

        QGraphicsObject.mouseReleaseEvent(self, event)

#        position connections precisely after fast node move
        self.moveConnections()

    #-------------------------------------------------------------------------
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):

        # bring all the colliding nodes to background
        overlapItems = self.collidingItems();

        for item in overlapItems:
            if(item.zValue() > 0.0):
                item.setZValue(0.0)

        #bring this node forward
        self.setZValue(1.0)

        self._node.nodeGeometry().setHovered(True)

        self.update()

        self._scene.nodeHovered.emit(self.node(),  event.screenPos())
        event.accept()

    #-------------------------------------------------------------------------
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):

        self._node.nodeGeometry().setHovered(False)

        self.update()

        self._scene.nodeHoverLeft.emit(self.node())

        event.accept()

    #-------------------------------------------------------------------------
    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent):

        pos = event.pos()
        geom = self._node.nodeGeometry()

        if(self._node.nodeDataModel().resizable() and
                    geom.resizeRect().contains(
                    QPoint(pos.x(), pos.y()))):

            self.setCursor(QCursor(Qt.SizeFDiagCursor))

        else:

            self.setCursor(QCursor())

        self.update()
        event.accept()

    #-------------------------------------------------------------------------
    def mouseDoubleClickEvent(self, event: QGraphicsSceneHoverEvent):

        QGraphicsItem.mouseDoubleClickEvent(self, event)

        self._scene.nodeDoubleClicked.emit(self.node())

    #-------------------------------------------------------------------------
    def contextMenuEvent(self,  event: QGraphicsSceneContextMenuEvent):
        self._node.nodeContextMenu(node(),  mapToScene(event.pos()))
##----------------------------------------------------------------------------

