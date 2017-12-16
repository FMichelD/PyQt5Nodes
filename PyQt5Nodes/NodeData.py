# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from abc import abstractmethod

#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *


class NodeDataType(object):
    def __init__(self):
        super().__init__()
        
        self.id = ""
        self.name = ""

#-----------------------------------------------------------------------------
class NodeData(object):
    
    def __init__(self):
        super().__init__()
        
        self.nodeDataType = NodeDataType()
        self.id = self.nodeDataType.id
        self.name = self.nodeDataType.id
    
    @abstractmethod
    def sameType(self, nodeData) -> bool:
        return(self.type().id == self.nodeData.type().id)

    #-------------------------------------------------------------------------
    @abstractmethod
    def type(self):
        pass
