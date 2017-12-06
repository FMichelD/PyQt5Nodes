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
        numberData = IntegerData(nodeData)
        
        if(portIndex == 0):
            self._integer = numberData
            
        if(self._integer):
            self._decimal = DecimalData(self._integer.number())
            
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return None
    
