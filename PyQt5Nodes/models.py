# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtWidgets import QWidget

from NodeData import *
from NodeDataModel import *
from PortType import *

class MyNodeData(NodeData):
    
    #override
    def type(self) -> NodeDataType:

        ndt = NodeDataType()
        
        ndt.id = "MyNodeData"
        ndt.name =  "My Node Data"
        
        return ndt

##-----------------------------------------------------------------------------
class SimpleNodeData(NodeData):
    
    #override
    def type(self) -> NodeDataType:
        
        ndt = NodeDataType()
        
        ndt.id = "SimpleNodeData"
        ndt.name =  "Simple Node Data"

        return ndt

##-----------------------------------------------------------------------------
class NaiveDataModel(NodeDataModel):
    
#    def __init__(self):
#        self._caption = "Naive Data Model"
    
    def setCaption(self,  caption):
        self._caption = caption

    def caption(self) -> str:

        return self._caption

    #-------------------------------------------------------------------------
    def name(self) -> str:

        return "NaiveDataModel"

    #-------------------------------------------------------------------------
    def clone(self) -> NodeDataModel:

        return NaiveDataModel()

    #-------------------------------------------------------------------------
    def nPorts(self, portType: PortType) -> int:

        result = 1

        if(portType == PortType.In):

            result = 2

        elif(portType == PortType.Out):

            result = 2

        else:
            pass
        
        return result
        
    #-------------------------------------------------------------------------
    def dataType(self, portType: PortType, portIndex: PortIndex)-> NodeDataType:

        if(portType == PortType.In):
            if(portIndex == 0):
                return SimpleNodeData().type()
            elif(portIndex == 1):
                return MyNodeData().type()
            else:
                pass
        elif(portType == PortType.Out):
            if(portIndex == 0):
                return MyNodeData().type()
            elif(portIndex == 1):
                return SimpleNodeData().type()
            else:
                pass            

    #-------------------------------------------------------------------------
    def outData(self, port: PortType) -> NodeData:

        if(port < 1):
            return MyNodeData

        return SimpleNodeData

    #-------------------------------------------------------------------------
    def setInData(self, nodeData: NodeData, port: PortIndex):
        pass

    #-------------------------------------------------------------------------
    def embeddedWidget(self) -> QWidget:
        return None
        
#-----------------------------------------------------------------------------
class Otro(NodeDataModel):
    
    def caption(self) -> str:
        return "Otro"

    #-------------------------------------------------------------------------
    def name(self) -> str:
        return "Otro"

    #-------------------------------------------------------------------------
    def clone(self) -> NodeDataModel:
        return Otro()

    #-------------------------------------------------------------------------
    def nPorts(self, portType: PortType) -> int:
        result = 1

#        if(portType == PortType.In):
#
#            result = 1
#
#        elif(portType == PortType.Out):
#
#            result = 1
#
#        else:
#            pass
        
        return result
        
    #-------------------------------------------------------------------------
    def dataType(self, portType: PortType, portIndex: PortIndex)-> NodeDataType:

        if(portType == PortType.In):
            if(portIndex == 0):
                return MyNodeData().type()
            elif(portIndex == 1):
                return SimpleNodeData().type()
            else:
                pass
        elif(portType == PortType.Out):
            if(portIndex == 0):
                return MyNodeData().type()
            elif(portIndex == 1):
                return SimpleNodeData().type()
            elif(portIndex == 2):
                return SimpleNodeData().type()
            else:
                pass            

    #-------------------------------------------------------------------------
    def outData(self, port: PortType) -> NodeData:

        if(port < 1):
            return MyNodeData

        return SimpleNodeData

    #-------------------------------------------------------------------------
    def setInData(self):
        pass

    #-------------------------------------------------------------------------
    def embeddedWidget(self) -> QWidget:
        return None
