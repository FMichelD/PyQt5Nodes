# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.NodeData import *

class IntegerData(NodeData):
    def __init__(self, nodeData:NodeData=None, num:float=0.0):
        super().__init__()
        
         #do cast form NodeData to IntegerData
        if(isinstance(nodeData, NodeData) and not isinstance(nodeData, IntegerData)):
            self.__dict__ = nodeData.__dict__
            self._number = None
        #do "cast" from IntegerData to IntegerData
        elif(isinstance(nodeData, IntegerData)):
            self._number = nodeData.number()
        #creata a new IntegerData instance
        else:            
            self._number = num
    
    #--------------------------------------------------------------------------
    #override
    def type(self):
        ndt = NodeDataType()
        
        ndt.id = "integer"
        ndt.name = "Integer"
        
        return ndt
    
    #--------------------------------------------------------------------------
    def number(self):
        return self._number
    
    #--------------------------------------------------------------------------
    def numberAsText(self):
        return str(self._number) 
    
