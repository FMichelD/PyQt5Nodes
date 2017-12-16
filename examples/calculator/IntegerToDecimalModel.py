# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtGui import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.PortType import *

from DecimalData import *
from IntegerData import *

class IntegerToDecimalModel(NodeDataModel):
    def __init__(self):
        super().__init__()
        
        self._decimal = None
        self._integer = None
        
    #--------------------------------------------------------------------------
    #override
    def caption(self):
        return "Integer to decimal"

    def setCaption(self, caption:str):
        self._caption = caption
        
    #--------------------------------------------------------------------------
    #override
    def captionVisible(self):
        return False
    
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "IntegerToDecimal"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return IntegerToDecimalModel()
    
    #--------------------------------------------------------------------------
    #override
    def save(self):
        modelJson = dict()
        
        modelJson["name"] = name()
        
        return modelJson
        
    #--------------------------------------------------------------------------
    #override
    def nPorts(self,  portType:PortType):
        result = 1
        
        if(portType == PortType.In):
            result = 1
        elif(portType == PortType.Out):
            result = 1
        
        return result
        
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType:PortType, portIndex:PortIndex):
        if(portType == PortType.In):
            return IntegerData().type()
        
        return DecimalData().type()
        
    #--------------------------------------------------------------------------
    #override
    def outData(self, port:PortIndex):
        return self._decimal
        
    #--------------------------------------------------------------------------
    #override
    def setInData(self, nodeData:NodeData, portIndex:PortIndex):
        if(isinstance(nodeData, NodeData) and not isinstance(nodeData, IntegerData)):
            numberData = None
        elif(isinstance(nodeData, IntegerData)):
            numberData = nodeData
        else:
            numberData = None
            
        if(portIndex == 0):
            self._integer = numberData
            
        if(self._integer):
            self._decimal = DecimalData(num=self._integer.number())
            
        outPortIndex = 0
        
        self.dataUpdated.emit(self, outPortIndex)
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return None
    
