# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.PortType import *

from IntegerData import *

class NumberDisplayDataModelInteger(NodeDataModel):
    def __init__(self):
        super().__init__()
        
        self._label = QLabel()
        self._label.setMargin(3)
#        self._label.setText("0.00000")
        self._label.setMinimumSize(60,  21)
#        print(self._label.sizeHint().width(),  self._label.sizeHint().height())
        
        self.modelValidationState = NodeValidationState.WARNING
        self.modelValidationError = "Missing or incorrect inputs"
        
    #--------------------------------------------------------------------------
    #override
    def captionVisible(self):
        return False
    
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "Integer Result"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return NumberDisplayDataModelInteger()
    
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
        return IntegerData().type()
        
    #--------------------------------------------------------------------------
#    #override
#    def outData(self, port:PortIndex):
#        ptr = NodeData
#        return ptr
        
    #--------------------------------------------------------------------------
    #override
    def setInData(self, nodeData:NodeData, portIndex:PortIndex):
        
        if(not isinstance(nodeData, IntegerData)):
            numberData = None
        else:
            numberData = nodeData
        
        if(numberData):
            self.modelValidationState = NodeValidationState.VALID
            self.modelValidationError = ""
            self._label.setText(numberData.numberAsText())
        else:
            self.modelValidationState = NodeValidationState.WARNING
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
