# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *

class DecimalData(NodeData):
    def __init__(self, nodeData:NodeData=None,  num:float=0.0):
        super().__init__()
    
        if(isinstance(nodeData, NodeData)):
            self.__dict__ = nodeData.__dict__
            
        self._number = num
        
    #--------------------------------------------------------------------------
    #override
    def type(self):
        NodeDataType.id = 'decimal'
        NodeDataType.name = 'Decimal'
        
        return NodeDataType
        
    #--------------------------------------------------------------------------
    def number(self):
        return self._number
    
    #--------------------------------------------------------------------------
    def numberAsText(self):
        return '{:f}'.format(self._number)
