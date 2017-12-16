# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *

from MathOperationDataModel import *
from DecimalData import *

class DivisionModel(MathOperationDataModel):
    def __init__(self):
        super().__init__()
    
    #--------------------------------------------------------------------------
    def __del__(self):
        pass
    
    #--------------------------------------------------------------------------
    def caption(self):
        return "Division"
    
    #--------------------------------------------------------------------------
    def portCaptionVisible(self, portType: PortType, portIndex: PortIndex):
        return True
    
    #--------------------------------------------------------------------------
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
    def name(self):
        return "Division"
    
    #--------------------------------------------------------------------------
    def clone(self):
        return DivisionModel()
    
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
            self._result = DecimalData(num=(n1.number() / n2.number()))
        else:
            self.modelValidationState = NodeValidationState.WARNING
            self.modelValidationError = "Missing or incorrect inputs"
            self._result = None
        
        self.dataUpdated.emit(self, outPortIndex)


#        outPortIndex = 0
#        
#        n1 = self._number1
#        n2 = self._number2
#        
#        if(n1 and n2):
#            self.modelValidationState = NodeValidationState.VALID
#            self.modelValidationError = ""
#            self._result = DecimalData(num=(n1.number() + n2.number()))
#        else:
#            self.modelValidationState = NodeValidationState.WARNING
#            self.modelValidationError = "Missing or incorrect inputs"
#            self._result = None
#            
#        self.dataUpdated.emit(self, outPortIndex)
