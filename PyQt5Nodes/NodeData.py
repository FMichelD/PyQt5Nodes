# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from abc import abstractmethod

#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *


class NodeDataType(object):
    id = ""
    name = ""

#-----------------------------------------------------------------------------
class NodeData(object):
    
    nodeDataType = NodeDataType()
    id = nodeDataType.id
    name = nodeDataType.id
    
    @abstractmethod
    def sameType(self, nodeData) -> bool:

        return(self.type().id == nodeData.type().id)

    #-------------------------------------------------------------------------
    @abstractmethod
    def type(self):
        return 0
