# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *

from MathOperationDataModel import *
from DecimalData import *

class ModuloModel(NodeDataModel):
    def __init__(self):
        super().__init__(self)
    
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
    def nPorts(self, portType:PortType):
        result = 1
        
        if(portType == PortType.In):
            result = 2
        elif(portType == PortType.Out):
            result = 1
            
        return result
        
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType:PortType,  portCaption:PortIndex):
        return IntergerData().type()
        
    #--------------------------------------------------------------------------
    #override
    def outData(self,  portIndex:PortIndex):
        return self._result
        
    #--------------------------------------------------------------------------
    #override
    def setInData(self, nodeData:NodeData, portIndex:PortIndex):
        numberData = IntergerData(nodeData)
        
        if(portIndex == 0):
            self._number1 = numberData
        else:
            self._number2 = numberData
        
        outPortIndex = 0
        
        n1 = self._number1.lock()
        n2 = self._number2.lock()
        
        if(n2 and (n2.number() == 0.0)):
            self.modelValidationState = NodeValidationState.Error
            self.modelValidationError = "Division by zero error"
            self._result.reset()
        elif(n1 and n2):
            self.modelValidationState = NodeValidationState.Valid
            self.modelValidationError = ""
            self._result = DecimalData(n1.number() % n2.number())
        else:
            self.modelValidationState = NodeValidationState.Warning
            self.modelValidationError = "Missing or incorrect inputs"
            self._result.reset()
        
        dataUpdated.emit(outPortIndex)
            
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return None
    
    #--------------------------------------------------------------------------
    #override
    def validationState(self):
        return self.modelValidationState

    #--------------------------------------------------------------------------
    #override
    def validationMessage(self):
        return self.modelValidationError
        
