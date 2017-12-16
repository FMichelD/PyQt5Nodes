# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *

from MathOperationDataModel import *
from DecimalData import *
from IntegerData import *

class ModuloModel(MathOperationDataModel):
    def __init__(self):
        super().__init__()
        
#        self.modelValidationState = NodeValidationState.ERROR
#        self.modelValidationError = "Division by zero error"
        
#        self._number1 = None
#        self._number2 = None
#        self._result = None
#        
    #--------------------------------------------------------------------------
    def __del__(self):
        pass
    
    #--------------------------------------------------------------------------
    #override
    def caption(self):
        return "Modulo"

    #--------------------------------------------------------------------------
    #override
    def portCaptionVisible(self, portType: PortType, portIndex: PortIndex):
        return True
    
    #--------------------------------------------------------------------------
    #override
    def portCaption(self, portType: PortType, portIndex: PortIndex):
        if(portType == PortType.In):
            if(portIndex == 0):
                return "Dividend"
            elif(portIndex == 1):
                return "Divisor"
        elif(portType == PortType.Out):
            return "Result"

        return ""
        
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "Modulo"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return ModuloModel()
    
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType:PortType,  portCaption:PortIndex):
        return IntegerData().type()
    
    #--------------------------------------------------------------------------
    #override
    def setInData(self, data:NodeData, portIndex:PortIndex):
        
        if(isinstance(data, NodeData) and not isinstance(data, IntegerData)):
            numberData = None
        elif(isinstance(data, IntegerData)):
            numberData = data
        
        if(portIndex == 0):
            self._number1 = numberData
        else:
            self._number2 = numberData
    
        self.compute()
        
    #--------------------------------------------------------------------------
    #override
    def compute(self):
        outPortIndex = 0
        
        n1 = self._number1
        n2 = self._number2
        
        if(n2 and (n2.number() == 0.0)):
            self.modelValidationState = NodeValidationState.ERROR
            self.modelValidationError = "Division by zero error"
            self._result = None
        elif(n1 and n2):
            self.modelValidationState = NodeValidationState.VALID
            self.modelValidationError = ""
            self._result = IntegerData(num=(n1.number() % n2.number()))
        else:
            self.modelValidationState = NodeValidationState.WARNING
            self.modelValidationError = "Missing or incorrect inputs"
            self._result = None
        
        self.dataUpdated.emit(self, outPortIndex)
