# -*- coding: utf-8 -*-
# !/usr/bin/env python3



from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.PortType import *

from DecimalData import *

class MathOperationDataModel(NodeDataModel):
    def __init__(self):
        super().__init__()
        
        self._number1 = DecimalData()
        self._number2 = DecimalData()
        
        self._result = DecimalData()
        
        self.modelValidationState = NodeValidationState.WARNING
        self.modelValidationError = "Missing or incorrect inputs"
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def __del__(self):
        pass    
    
    #--------------------------------------------------------------------------
    def nPorts(self,  portType: PortType):
        result = int()
        
        if(portType == PortType.In):
            result = 2
        else:
            result = 1
            
        return result
        
    #--------------------------------------------------------------------------
    def dataType(self,  portType: PortType, portIndex: PortIndex):
        return DecimalData().type()
        
    #--------------------------------------------------------------------------
    def outData(self, port: PortIndex):
        return NodeData(self._result)
    
    #--------------------------------------------------------------------------
    def setInData(self, data: NodeData,  portIndex: PortIndex):
        numberData = DecimalData(data)
        
        if(portIndex == 0):
            self._number1 = numberData
        else:
            self._number2 = numberData
            
        self.compute()
    
    #--------------------------------------------------------------------------
    def validationState(self):
        return self.modelValidationState
        
    #--------------------------------------------------------------------------
    def validationMessage(self):
        return self.modelValidationError
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def compute(self):
        pass
        
    #--------------------------------------------------------------------------
    def embeddedWidget(self):
        return None
