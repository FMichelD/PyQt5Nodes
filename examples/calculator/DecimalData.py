# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *

class DecimalData(NodeData):
    def __init__(self, nodeData:NodeData=None,  num:float=0.0):
        super().__init__()
    
        #do cast form NodeData to DecimalData
        if(isinstance(nodeData, NodeData) and not isinstance(nodeData, DecimalData)):
            self.__dict__ = nodeData.__dict__
            self._number = None
        #do "cast" from DecimalData to DecimalData
        elif(isinstance(nodeData, DecimalData)):
            self._number = nodeData.number()
        #creata a new DecimalData instance
        else:            
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
        if(self._number is not None):
            return '{:f}'.format(self._number)
