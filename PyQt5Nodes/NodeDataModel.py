# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from typing import *
from abc import  abstractmethod
from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5Nodes.Serializable import *
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.PortType import *
from PyQt5Nodes.StyleCollection import *

class NodeValidationState(Enum):
    ERROR = -1
    WARNING = 0
    VALID = 1

class ConnectionPolicy(Enum):
    One = 1
    Many = 0

#-----------------------------------------------------------------------------
class NodeDataModel(QObject, Serializable):

    _captionVisibility = True
    _portCaptionVisibility = False

    def __init__(self):
        super().__init__()
        
        self._nodeStyle = StyleCollection.nodeStyle()
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def caption(self) -> str:
        pass

    #--------------------------------------------------------------------------
    def captionVisible(self) -> bool:
        return True

    #--------------------------------------------------------------------------
    def setCaptionVisible(self, visible: bool):
        self._captionVisibility = visible

    #--------------------------------------------------------------------------
    def portCaption(self, portType: PortType, portIndex: PortIndex) -> str:
        return ("")

    #--------------------------------------------------------------------------
    def portCaptionVisible(self, portType: PortType, portIndex: PortIndex):
        return False

    #--------------------------------------------------------------------------
    def setPortCaptionVisible(self, visible: bool):
        self._portCaptionVisibility = visible

    #--------------------------------------------------------------------------
    def save() -> dict:
        modelJson = dict()
        
        modelJson["name"] = self.name()

        return modelJson
        
    #--------------------------------------------------------------------------
    def portOutConnectionPolicy(self, PortIndex): 
        return ConnectionPolicy.Many;
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def name(self):        
        pass
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def clone(self):        
        pass

    #--------------------------------------------------------------------------
    @abstractmethod
    def nPorts(self, portType: PortType) -> int:        
        pass

    #--------------------------------------------------------------------------
    @abstractmethod
    def dataType(self, portType: PortType, portIndex: PortIndex) -> NodeDataType:        
        pass

    #--------------------------------------------------------------------------
    #@abstractmethod
    def setInData(self, nodeData: NodeData, port: PortIndex):        
        pass

    #--------------------------------------------------------------------------
    @abstractmethod
    def outData(self, port: PortIndex) -> NodeData:        
        pass

    #--------------------------------------------------------------------------
    @abstractmethod
    def embeddedWidget(self) -> QWidget:        
        pass

    #--------------------------------------------------------------------------
    def nodeStyle(self):
        return self._nodeStyle

    #--------------------------------------------------------------------------
    def setNodeStyle(self, style):
        self._nodeStyle = style
        
    #--------------------------------------------------------------------------
    def resizable(self) -> bool:
        return False

    #--------------------------------------------------------------------------
    def validationState(self) -> NodeValidationState:
        return NodeValidationState.VALID

    #--------------------------------------------------------------------------
    def validationMessage(self):
        return str('')

    #--------------------------------------------------------------------------
    def painterDelegate(self):
        return None
        
    #--------------------------------------------------------------------------
    #Signals

    dataUpdated = pyqtSignal(object, PortIndex)

    dataInvalidated = pyqtSignal(object, PortIndex)

    computingStarted = pyqtSignal()

    computingFinished = pyqtSignal() 

#------------------------------------------------------------------------------

###############################################################################
#Only for tests
#
#if __name__ == "__main__":
#
#    from NodeDataModel import *
#    from PyQt5.QtCore import *
#
#    class Ndm(NodeDataModel):
#
#        def caption(self) -> str:
#            return "Ndm_caption"
#
#        def name(self) -> str:
#            return "Ndm_name"
#
#        def clone(self) -> NodeDataModel:
#            return Ndm()
#
#        def nPorts(self, portType: PortType) -> int:
#            return 10
#
#        def dataType(self, portType: PortType, portIndex: PortIndex) -> NodeDataType:
#            return MyNodeData().type()
#
#        def outData(self, port: PortIndex) -> NodeData:
#            return MyNodeData()
#
#        def setInData(self):
#            pass
#
#        def embeddedWidget(self) -> QWidget:
#            return None
#
#    class Node(QObject):
#        
#        def __init__(self,  ndm: NodeDataModel):
#            super().__init__()
#            
#            self._ndm = ndm                       
#            
#            self._ndm.dataUpdated.connect(self.testConn)            
#            
#            
#        def testConn(self, i: int):
#            #print("Connection OK: i = {}".format(i))
#
#
#ndm = Ndm()
#
#node = Node(ndm)
#
#ndm.dataUpdated.emit(100)
#
##print(ndm == node._ndm)
