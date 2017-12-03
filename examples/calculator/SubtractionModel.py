# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Node.NodeDataModel import *

from MathOperationDataModel import *
from DecimalData import *

class Subtraction(MathOperationDataModel):
    def __init__(self):
        super().__init__(self)
    
    #--------------------------------------------------------------------------
    def __del__(self):
        pass
    
    #--------------------------------------------------------------------------
    def caption(self):
        return "Subtraction"
    
    #--------------------------------------------------------------------------
    def portCaptionVisible(self, portType: PortType, portIndex: PortIndex):
        return True
    
    #--------------------------------------------------------------------------
    def portCaption(self, portType: PortType, portIndex: PortIndex):
        if(portType == PortType.In):
            if(portIndex == 0):
                return "Minuend"
            elif(portIndex == 1):
                return "Subtrahend"
        elif(portType == PortType.Out):
            return "Result"

        return ""
        
    #--------------------------------------------------------------------------
    def name(self):
        return "Subtraction"
    
    #--------------------------------------------------------------------------
    def clone(self):
        return SubtractionModel()
    
    #--------------------------------------------------------------------------
    #override
    def comput(self):
        outPortIndex = 0
        
        n1 = self._number1.lock()
        n2 = self._number2.lock()
        
        if(n1 and n2):
            self.modelValidationState = NodeValidationState.Valid
            self.modelValidationError = ""
            self._result = DecimalData(n1.number() - n2.number())
        else:
            self.modelValidationState = NodeValidationState.Warning
            self.modelValidationError = "Missing or incorrect inputs"
            self._result.reset()
        
        dataUpdated.emit(outPortIndex)
