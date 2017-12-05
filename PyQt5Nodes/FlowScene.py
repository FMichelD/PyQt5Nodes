# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtWidgets import  *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5Nodes.Node import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeGraphicsObject import *
from PyQt5Nodes.NodeStyle import *

from PyQt5Nodes.DataModelRegistry import *
from PyQt5Nodes.PortType import *

from PyQt5Nodes.Connection import *
from PyQt5Nodes.ConnectionGraphicsObject import *


class FlowScene(QGraphicsScene):
    def __init__(self, registry):
        super(FlowScene,  self).__init__()

        self._nodes = dict()
        self._connections = dict()
        self._registry = DataModelRegistry()

        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        self._registry = registry

#-----------------------------------------------------------------------------
    def __del__(self):
        self.clearScene()

#-----------------------------------------------------------------------------
    def createConnection(self, *args):
        signature = tuple(arg.__class__ for arg in args)

        typemap = { (PortType, Node, PortIndex) : self.createConnectionPtNPi,
                (Node, PortIndex, Node, PortIndex) : self.createConnectionNPiNPi }

        if signature in typemap:
          return typemap[signature](*args)
        else:
          raise TypeError("Invalid type signature: {0}".format(signature))

#-----------------------------------------------------------------------------
    def createConnectionPtNPi(self, connectedPort: PortType, node,
                        portIndex: PortIndex):
        connection = Connection(connectedPort, node, portIndex)

        cgo = ConnectionGraphicsObject(self, connection)

        # after this function connection points to node port
        connection.setGraphicsObject(cgo)

        self._connections[connection.id()] = connection

        self.connectionCreated.emit(connection)

        return connection

#-----------------------------------------------------------------------------
    def createConnectionNPiNPi(self, nodeIn, portIndexIn: PortIndex,
                                nodeOut, portIndexOut: PortIndex):

        connection = Connection(nodeIn, portIndexIn, nodeOut, portIndexOut)

        cgo = ConnectionGraphicsObject(connection)

        nodeIn.nodeState().setConnection(PortType.In, portIndexIn, connection)
        nodeOut.nodeState().setConnection(PortType.Out, portIndexOut, connection)

        # after this function connection points to node port
        connection.setGraphicsObject(cgo)

        # trigger data propagation
        nodeOut.onDataUpdated(portIndexOut)

        self._connections[connection.id()] = connection

        self.connectionCreated.emit(connection)

        return connection

#-----------------------------------------------------------------------------
    def restoreConnection(self, connectionJson):

        nodeInId = QUid(connectionJson["in_id"].toString())
        nodeOutId = QUid(connectionJson["in_id"].toString())

        portIndexIn = connectionJson["in_index"].toInt()
        portIndexOut = connectionJson["out_index"].toInt()

        nodeIn = _nodes[nodeInId].get()
        nodeOut = _nodes[nodeOutId].get()

        return createConnection(nodeIn, portIndexIn, nodeOut, portIndexOut)

#-----------------------------------------------------------------------------
    def deleteConnection(self, connection: Connection):
        self.connectionDeleted.emit(connection)
        connection.removeFromNodes()
        self._connections.pop(connection.id())

        cgo = connection.getConnectionGraphicsObject()
        cgo.__del__()

#-----------------------------------------------------------------------------
    def createNode(self, dataModel: NodeDataModel):
        node = Node(dataModel)
        ngo = NodeGraphicsObject(self, node)
        node.setGraphicsObject(ngo)

        self._nodes[node.id()] = node

        self.nodeCreated.emit(node)

        return node

#-----------------------------------------------------------------------------
    def restoreNode(self, nodeJson: dict):
        modelName = nodeJson["model"].toObject()["name"].toString()

        dataModel = registry().create(modelName)

        if(not dataModel):
            raise ReferenceError("No registered model with name {}".format(
                    modelName.toLocal8Bit().data()))

        node = Node(dataModel)
        ngo = NodeGraphicsObject(self, node)
        node.setGraphicsObject(ngo)

        node.restore(nodeJson)

        self._nodes[node.id()] = node

        self.nodeCreated.emit(node)

        return node

    #-----------------------------------------------------------------------------
    def removeNode(self, node):

        # call signal
        self.nodeDeleted.emit(node)

        #-----------------------------------------------------------------------------
        def deleteConnections(portType: PortType):
            nodeState = node.nodeState()
            nodeEntries = nodeState.getEntries(portType)

            for connection in nodeEntries:
                for id, conn in connection.items():
                    self.deleteConnection(conn)
                    break


        deleteConnections(PortType.In)
        deleteConnections(PortType.Out)

        nd = self._nodes.get(node.id())
        ngo = nd.nodeGraphicsObject()

        self._nodes.pop(node.id())
        ngo.__del__()

#-----------------------------------------------------------------------------
    def registry(self) -> DataModelRegistry:
        return self._registry

#-----------------------------------------------------------------------------
    def setRegistry(self, registry: DataModelRegistry):
        self._registry = registry

#-----------------------------------------------------------------------------
    def iterateOverNodes(self, visitor):
        for node in self._nodes:
            visitor(node.second.get())

#-----------------------------------------------------------------------------
    def iterateOverNodeData(self, visitor: NodeDataModel):
        for node in self._nodes:
            visitor(node.second.NodeDataModel())

#-----------------------------------------------------------------------------
    def iterateOverDataDependentOrder(self, visitor: NodeDataModel):
        visiteNodesSet = []

        #-----------------------------------------------------------------------------
        # A leaf node is a node with no input ports, or all possible input ports empty
        def isNodeLeaf(node, model: NodeDataModel):

            for i in range(0, model.nPorts(PortType.In)):
                connections = node.nodeState().connections(PortType.In, i)

                if(not connections.empty()):
                    return False

                return True

        # iterate over "leaf" nodes
        for self._node in self._nodes:
            node = self._node.second
            model = node.nodeDataModel

            if( self.isNodeLeaf(node, model)):
                visitor(model)
                visiteNodesSet.insert(node.id())

        #-----------------------------------------------------------------------------
        def areNodeInputVisitedBefore(node, model: NodeDataModel):

            for i in range(0, model.nPorts(PortType.In)):
                connections = node.nodeState().connections(PortType.In, i)

                for conn in connections:
                    if(visiteNodesSet.find(conn.second.getNode(PortType.Out).id()) ==
                        visiteNodesSet.end()):
                        return False

                return True

        while(self._nodes.size() != visiteNodesSet.size()):
            for self._node in self._nodes:
                node = self._node.second

                if(visiteNodesSet.find(node.id()) != visiteNodesSet.end()):
                    continue

                model = node.nodeDataModel()

                if(areNodeInputVisitedBefore(node, model)):
                    visitor(model)
                    visiteNodesSet.insert(node.id())

#-----------------------------------------------------------------------------
    def getNodePosition(self, node) -> QPointF:
        return node.nodeGraphicsObject().pos()

#-----------------------------------------------------------------------------
    def setNodePositon(self, node, pos: QPointF):
        node.nodeGraphicsObject().setPos()
        node.nodeGraphicsObject().moveConnections()

#-----------------------------------------------------------------------------
    def getNodeSize(self, node) -> QSizeF:
        return QSizeF(node.nodeGEometry().width(), node.nodeGEometry().height())

#-----------------------------------------------------------------------------
    def nodes(self):
        return self._nodes

#-----------------------------------------------------------------------------
    def connections(self) -> Connection:
        return self._connections

#-----------------------------------------------------------------------------
    def selectNodes(self) -> list:
        graphicsItems = selectedItems()

        ret = []

        for item in graphicsItems:
            ngo = item

            if(not ngo is None):
                ret.append(ngo.node())

        return ret

#-----------------------------------------------------------------------------
    def clearScene(self):
        # Manual node cleanup. Simply clearing the holding datastructures doesn't work, the code crashes when
        # there are both nodes and connections in the scene. (The data propagation internal logic tries to propagate
        # data through already freed connections.)
        nodesToDelete = []

        for node in self._nodes:
            nodesToDelete.append(node.second.get())

        for node in nodesToDelete:
            self.removeNode(node)
#
#    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
#        #print("mouse on scene")
#-----------------------------------------------------------------------------
    def save(self):
        fileName = QFileDialog.getSaveFileName(None, "Open Flow Scene",
                                                QDir.homePath(),
                                                "Flow Scene Files (*.flow)")

        if(not fileName.isEmpty()):
            if(not fileName.endWith("flow", Qt.CaseInsensitive)):
                fileName += ".flow"

            file = QFile(fileName)

            if(file.open(QIODevice.WriteOnly)):
                file.write(saveToMemory())

#-----------------------------------------------------------------------------
    def load(self):

        self.clearScene()

        fileName = QFileDialog.getOpenFileName(None,
                                                "Open Flow Scene",
                                                QDir.homePath(),
                                                "Flow Scene Files (*.flow)")

        if(not QFileInfo.exists(fileName)):
            return

        file = QFile(fileName)

        if(not file.open(QIODevice.ReadOnly)):
            return

        wholeFile = file.readAll()

        self.loadFromMemory(wholeFile)

#-----------------------------------------------------------------------------
    def saveToMemory(self) -> QByteArray:

        sceneJson = QJsonObject()

        nodesJsonArray = QJsonArray()


        for pair in self._nodes:
            node = pair.second;

            nodesJsonArray.append(node.save())

        sceneJson["nodes"] = nodesJsonArray

        connectionJsonArray = QJsonArray();

        for pair in self._connections:
            connection = pair.second

            connectionJson = connection.save()

            if(not connectionJson.isEmpty()):
                connectionJsonArray.append(connectionJson)

        sceneJson["connections"] = connectionJsonArray

        document = QJsonObject(sceneJson)

        return document.toJson()

#-----------------------------------------------------------------------------
    def loadFromMemory(self, data: QByteArray):

        jsonDocument = QJsonDocument.fromJson(data).object()

        nodesJsonArray = jsonDocument["nodes"].toArray()

        for i in range(0, nodesJsonArray.size()):
            self.restoreNode(nodesJsonArray[i].toObject())

        connectionJsonArray = jsonDocument["connections"].toArray()

        for i in range(0, connectionJsonArray.size()):
            self.restoreConnection(connectionJsonArray[i]).toObject

#-----------------------------------------------------------------------------
    def locateNodeAt(self, scenePoint: QPointF, scene,
                     viewTransform: QTransform):

        items = list(scene.items(scenePoint, Qt.IntersectsItemShape,
                     Qt.DescendingOrder, viewTransform))

        filteredItems = list()
        for item in items:
            if(isinstance(item, NodeGraphicsObject)):
                filteredItems.append(item)

#        std::copy_if(items.begin(),
#            items.end(),
#            std::back_inserter(filteredItems),
#            [] (QGraphicsItem * item)
#            {
#              return (dynamic_cast<NodeGraphicsObject*>(item) != nullptr);
#            });

#        resultNode = None

        if(filteredItems): #if list not is empty then ...
            graphicsItem = next(iter(filteredItems))

#            ngo = NodeGraphicsObject(graphicsItem)
#
#            resultNode = ngo.node()
#
#        return resultNode

            return graphicsItem.node()
#-----------------------------------------------------------------------------
#    def itemNotIsNone(self, item):
#
#        if(not item is Node):
#            return item

    #-------------------------------------------------------------------------
    #Signals

    nodeCreated = pyqtSignal(Node)

    nodeDeleted = pyqtSignal(Node)

    connectionCreated = pyqtSignal(Connection)

    connectionDeleted = pyqtSignal(Connection)

    nodeMoved = pyqtSignal(Node, QPointF)

    nodeDoubleClicked = pyqtSignal(Node)

    connectionHovered = pyqtSignal(Connection, QPoint)

    nodeHovered = pyqtSignal(Node, QPoint)

    connectionHoverLeft = pyqtSignal(Connection)

    nodeHoverLeft = pyqtSignal(Node)

    #-------------------------------------------------------------------------
    #Slots
    @pyqtSlot(Node,  QPointF)
    def moveNode(self, node,  pos):
        self.nodeMoved.emit(node,  pos)
#-----------------------------------------------------------------------------

################################################################################
#if __name__ == "__main__":
#    from DataModelRegistry import *
#    from models import *
#
#    def registerDataModels():
#
#        ret = DataModelRegistry()
#
#        ret.registerModel(NaiveDataModel())
#
#        #print("registrando")
#
#        return ret
#
#    f = FlowScene(registerDataModels())
#
#    n = f.createNodes()
#
#    #print(type(n))
