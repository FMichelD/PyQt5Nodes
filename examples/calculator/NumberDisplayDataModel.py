# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.PortType import *

from DecimalData import *

class NumberDisplayDataModel(NodeDataModel):
    def __init__(self):
        super().__init__(self)
        
        self._label = QLable()
        self._label.setMargin(3)
        
        self.modelValidationState = NodeValidationState.Warning
        self.modelValidationError = "Missing or incorrect inputs"
        
    #--------------------------------------------------------------------------
    #override
    def caption(self):
        return "Result"
    
    #--------------------------------------------------------------------------
    #override
    def captionVisible(self):
        return False
    
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "Result"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return NumberDisplayDataModel()
    
    #--------------------------------------------------------------------------
    #override
    def nPorts(self, portType:PortType):
        result = 1
        
        if(portType == PortType.In):
            result = 1
        elif(portType == PortType.Out):
            result = 0
            
        return result
        
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType:PortType, portIndex:PortIndex):
        return DecimalData().type()
        
    #--------------------------------------------------------------------------
    #override
    def outData(self, port:PortIndex):
        ptr = NodeData
        return ptr
        
    #--------------------------------------------------------------------------
    #override
    def setInData(self, nodeData:NodeData, portIndex:PortIndex):
        numberData = DecimalData(nodeData)
        
        if(numberData):
            self.modelValidationState = NodeValidationState.Valid
            self.modelValidationError = ""
            self._label.setText(numberData.numberAsText())
        else:
            self.modelValidationState = NodeValidationState.Warning
            self.modelValidationError = "Missing or incorrect inputs"
            self._label.clear()
            
        self._label.adjustSize()
        
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return self._label
    
    #--------------------------------------------------------------------------
    #override
    def validationState(self):
        return self.modelValidationState
        
    #--------------------------------------------------------------------------
    #override
    def validationMessage(self):
        return self.modelValidationError
