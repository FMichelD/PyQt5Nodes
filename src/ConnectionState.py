# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *

from FlowScene import *
from Node import *
from PortType import *

##----------------------------------------------------------------------------
class ConnectionState(object):
    def __init__(self, port=PortType.No_One):
        self._requiredPort = None
        self._lastHoveredNode = None

    #-------------------------------------------------------------------------
    def __del__(self):
        self.resetLastHoveredNode()

    #-------------------------------------------------------------------------
    def interactWithNode(self, node):
        if(node):
            self._lastHoveredNode = node
        else:
            self.resetLastHoveredNode()

    #-------------------------------------------------------------------------
    def setLastHoveredNode(self,  node):
        self._lastHoveredNode = node

    #-------------------------------------------------------------------------
    def resetLastHoveredNode(self):
        if(self._lastHoveredNode):
            self._lastHoveredNode.resetReactionToConnection()

        self._lastHoveredNode = None

    #-------------------------------------------------------------------------
    def setRequiredPort(self, end: PortType):
        self._requiredPort = end

    #-------------------------------------------------------------------------
    def requiredPort(self):
        return self._requiredPort

    #-------------------------------------------------------------------------
    def requiresPort(self):
        return self._requiredPort != PortType.No_One

    #-------------------------------------------------------------------------
    def setNoRequiredPort(self):
        self._requiredPort = PortType.No_One

    #-------------------------------------------------------------------------
    def lastHoveredNode(self):
        return self._lastHoveredNode
##----------------------------------------------------------------------------

