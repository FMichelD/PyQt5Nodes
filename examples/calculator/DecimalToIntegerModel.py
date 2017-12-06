# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.PortType import *

from DecimalData import *
from IntegerData import *

class DecimalToIntegerModel(NodeDataModel):
    def __init__(self):
        super().__init__()
        
        self._decimal = DecimalData()
        self._integer = IntegerData()
        
    #--------------------------------------------------------------------------
    #override
    def caption(self):
        return "Decimal to integer"
    
    #--------------------------------------------------------------------------
    #override
    def captionVisible(self):
        return True
    
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "DecimalToInteger"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return DecimalToIntegerModel() 
    
    #--------------------------------------------------------------------------
    #override
    def save(self):
        modelJson = dict()
        
        modelJson["name"] = name()
        
        return modelJson
    
    #--------------------------------------------------------------------------
    #override
    def nPorts(self, portType: PortType):
        result = 1
        
        if(portType == PortType.In):
            result = 1
        elif(portType == PortType.Out):
            result = 1
        
        return result
        
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType: PortType, portIndex: PortIndex):
        if(portType == PortType.In):
            return DecimalData().type()
        
        return IntegerData().type()
    
    #--------------------------------------------------------------------------
    #override
    def outData(self, port: PortIndex):
        return self._integer
    
    #--------------------------------------------------------------------------
    #override
    def setInData(self, data: NodeData, portIndex: PortIndex):
        numberData = DecimalData(data)
        
        if(portIndex == 0):
            self._decimal = numberData
        
        if(self._decimal):
            self._integer = IntegerData(self._decimal.number())
            
        outPortIndex = 0
        
        dataUpdated.emit(outPortIndex)
    
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return None
