# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *

class IntegerData(NodeData):
    def __init__(self,  number:float=0.0):
        super().__init__()
        
        self._number = number
    
    #--------------------------------------------------------------------------
    #override
    def type(self):
        NodeDataType.id = "integer"
        NodeDataType.name = "Integer"
        
        return NodeDataType
    
    #--------------------------------------------------------------------------
    def number(self):
        return self._number
    
    #--------------------------------------------------------------------------
    def numberAsText(self):
        return str(self._number) 
    
