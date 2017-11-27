# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import logging

#from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject

#from Node import *
from PortType import *
#from FlowScene import *
from NodeState import *
from NodeGeometry import *
from NodeData import *
from NodeGraphicsObject import *
from NodeDataModel import *
#from ConnectionGraphicsObject import *
#from ConnectionState import *
from Serializable import *
from StyleCollection import *

class Node(QObject, Serializable):

    def __init__(self, dataModel: NodeDataModel):
        QObject.__init__(self)
        
        self._id = QUuid.createUuid()

        self._nodeDataModel = dataModel

        self._nodeState = NodeState(self._nodeDataModel)

        self._nodeGeometry = NodeGeometry(self._nodeDataModel)
        
        self._nodeStyle = StyleCollection.nodeStyle()

        self._nodeGraphicsObject = None

        self._nodeDataModel.dataUpdated.connect(self.onDataUpdated)
        
        self.nodeDataModel().setCaption(self.id().toString())

#-----------------------------------------------------------------------------
    @pyqtSlot()
    def propagateData(self, nodeData: NodeData, inPortIndex: PortIndex):
        
        self._nodeDataModel.setInData(nodeData, inPortIndex)

        # Recalculate the nodes visuals. A data change can result
        #    in the node taking more space than before, so this forces a recalculate+repaint on the affected node
        self._nodeGraphicsObject.setGeometryChanged()

        self._nodeGeometry.recalculateSize()

        self._nodeGraphicsObject.update()

        self._nodeGraphicsObject.moveConnections()

#-----------------------------------------------------------------------------
    @pyqtSlot()
    def onDataUpdated(self, index: PortIndex):        
        nodeData = self._nodeDataModel.outData(index)

        connections = self._nodeState.connections(PortType.Out, index)

        for c in connections.items():
            c[1].propagateData(nodeData)
            
#-----------------------------------------------------------------------------
    def save(self) -> dict:
        nodeJson = dict()

        nodeJson["id"] = self._id.toString()

        nodeJson["model"] = self._nodeDataModel.save()
        
   
        obj = dict()

        obj["x"] = self._nodeGraphicsObject.pos().x()
        obj["y"] = self._nodeGraphicsObject.pos().y()

        nodeJson["position"] = obj

        return nodeJson

#----------------------------------------------------------------------------- 
    def restore(self,  json: dict):
        self._id = QUuid(json["id"].toString())

        positionJson = json["position"]

        point = QPointf(float(positionJson["x"]), float(positionJson["y"]))

        self._nodeGraphicsObject.setPos(point)

        self._nodeDataModel.restore(json["model"])
         
#-----------------------------------------------------------------------------
    def id(self) -> QUuid:
        return self._id

#-----------------------------------------------------------------------------
    def reactToPossibleConnection(self, reactingPortType:PortType,
                                    reactingDataType: NodeDataType,
                                    scenePoint: QPointF):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\nNode.py: reactToPossibleConnection(...)')
#        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))
        
        
        t = self._nodeGraphicsObject.sceneTransform()

        p = t.inverted()[0].map(scenePoint)

        self._nodeGeometry.setDraggingPosition(p)


        self._nodeState.setReaction(ReactToConnectionState.REACTING,
                                                    reactingPortType,
                                                    reactingDataType)
        logging.debug("nodeState IsReacting?: {}".format(self._nodeState.isReacting()))
#-----------------------------------------------------------------------------
    def resetReactionToConnection(self):
        self._nodeState.setReaction(ReactToConnectionState.NOT_REACTING)
        self._nodeGraphicsObject.update()

#-----------------------------------------------------------------------------
    def nodeGraphicsObject(self) -> NodeGraphicsObject:
        return self._nodeGraphicsObject

#-----------------------------------------------------------------------------
    def setGraphicsObject(self, graphics: NodeGraphicsObject):
        self._nodeGraphicsObject = graphics
        self._nodeGeometry.recalculateSize()

#-----------------------------------------------------------------------------
    def nodeGeometry(self) -> NodeGeometry:
        return self._nodeGeometry

#-----------------------------------------------------------------------------
    def nodeState(self) -> NodeState:
        return self._nodeState

#-----------------------------------------------------------------------------
    def nodeDataModel(self) -> NodeDataModel:
        return self._nodeDataModel
        
#-----------------------------------------------------------------------------
    def nodeStyle(self) -> NodeStyle:        
        return self._nodeStyle
