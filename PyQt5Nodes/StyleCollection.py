# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from typing import *

#from PyQt5.QtWidgets import  *
#from DataModelRegistry import *

from PyQt5Nodes.FlowViewStyle import FlowViewStyle
from PyQt5Nodes.ConnectionStyle import ConnectionStyle
from PyQt5Nodes.NodeStyle import NodeStyle

##----------------------------------------------------------------------------
class StyleCollection(object):
       
    _flowViewStyle = FlowViewStyle()
    
    _nodeStyle = NodeStyle()

    _connectionStyle = ConnectionStyle()

    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    
    #-------------------------------------------------------------------------
    @staticmethod
    def nodeStyle():# -> NodeStyle:
       
        return StyleCollection._nodeStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def connectionStyle():# -> ConnectionStyle:

        return StyleCollection.instance()._connectionStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def flowViewStyle() -> FlowViewStyle:

        return StyleCollection.instance()._flowViewStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def setNodeStyle(nodeStyle: NodeStyle):

        StyleCollection.instance()._nodeStyle = nodeStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def setConnectionStyle(connectionStyle: ConnectionStyle):

        StyleCollection.instance()._connectionStyle = connectionStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def setFlowViewStyle(flowViewStyle: FlowViewStyle):

        StyleCollection.instance()._flowViewStyle = flowViewStyle

    #-------------------------------------------------------------------------
    @staticmethod
    def instance():# -> StyleCollection:

        collection = StyleCollection()
        
        return collection

##----------------------------------------------------------------------------
    
