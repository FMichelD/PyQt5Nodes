# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from abc import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *

from MathOperationDataModel import *
from DecimalData import *

class AdditionModel(MathOperationDataModel):
    def __init__(self):
        super().__init__()
        
    #--------------------------------------------------------------------------
    @abstractmethod
    def __del__(self):
        pass
    
    #--------------------------------------------------------------------------
    def caption(self):
        return "Addition"
    def setCaption(self, caption:str):
        self._caption = caption
    #--------------------------------------------------------------------------
    def name(self):
        return "Addition"
    
    #--------------------------------------------------------------------------
    def clone(self):
        return AdditionModel()

    #--------------------------------------------------------------------------
    #override
    def compute(self):
        outPortIndex = 0
        
        n1 = self._number1
        n2 = self._number2
        
        if(n1 and n2):
            self.modelValidationState = NodeValidationState.VALID
            self.modelValidationError = ""
            self._result = DecimalData(n1.number() + n2.number())
        else:
            self.modelValidationState = NodeValidationState.WARNING
            self.modelValidationError = "Missing or incorrect inputs"
            self._result.reset()
            
        dataUpdated.emit(outPortIndex)
        
        
