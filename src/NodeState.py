# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from typing import *
from enum import Enum

#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PortType import *
from NodeData import *
from NodeDataModel import *
from NodeState import *
from Connection import *

#-----------------------------------------------------------------------------
class ReactToConnectionState(Enum):

    REACTING = True
    NOT_REACTING = False

#-----------------------------------------------------------------------------
class NodeState(object):

#    ConnectionPtrSet = dict() #unordered_map<QUuid, Connection>
#    _inConnections = [ConnectionPtrSet] #vector<ConnectionPtrSet>
#    _outConnections = [ConnectionPtrSet]


    def __init__(self, model: NodeDataModel):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('NodeState.py: __init__(...)')
#        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))

        self._outConnections = [dict()] * model.nPorts(PortType.Out)

        self._inConnections = [dict()] * model.nPorts(PortType.In)

        self._reaction = ReactToConnectionState.NOT_REACTING

        self._reactingPortType = PortType(PortType.No_One)

        self._resizing = False

    #-----------------------------------------------------------------------------
    def getEntries(self, portType: PortType) -> dict:
        if(portType == PortType.In):
            return self._inConnections
        else:
            return self._outConnections

    #-----------------------------------------------------------------------------
    def connections(self, portType: PortType, portIndex: PortIndex) -> dict:
        connections = self.getEntries(PortType)
        return connections[portIndex]        

    #-----------------------------------------------------------------------------
    def setConnection(self, portType: PortType, portIndex: PortIndex,
                         connection: Connection):

        connections = self.getEntries(portType)

        connections[portIndex].update({connection.id(): connection})
#        connections[portIndex] = dict([(connection.id(), connection)])

    #-----------------------------------------------------------------------------
    def eraseConnection(self, portType: PortType, portIndex: PortIndex,
                        id: QUuid):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print("\nNodeState: eraseConnection(self)")
#        print('caller name:', calframe[1][3])
#        print('on:', calframe[1][1])
#        print('')
        
#        cgo = self.getEntries(portType)[portIndex].get(id).getConnectionGraphicsObject()
#        conn = self.getEntries(portType)[portIndex].get(id)
        self.getEntries(portType)[portIndex].pop(id)
        
#        cgo.__del__()
#        conn.connectionGeometry().__del__()
#        conn.__del__()
#        cgo = None
#        conn = None
    #-----------------------------------------------------------------------------
    def reaction(self):
        return self._reaction

    #-----------------------------------------------------------------------------
    def reactingPortType(self) -> PortType:
        return self._reactingPortType

    #-----------------------------------------------------------------------------
    def reactingDataType(self) -> NodeDataType:
        return self._reactingDatatype

    #-----------------------------------------------------------------------------
    def setReaction(self, reaction: ReactToConnectionState,
                    reactingPortType: PortType=PortType.No_One, 
                    reactingDataType: NodeDataType =NodeDataType()):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\nNodeState.py: setReaction(...)')
#        print('caller name: {} {}'.format(calframe[1][3], calframe[1][1]))
        
        self._reaction = reaction

        self._reactingPortType = reactingPortType

        self._reactingDatatype = reactingDataType

    #-----------------------------------------------------------------------------
    def isReacting(self) -> bool:
#        self._reaction = ReactToConnectionState.REACTING        
        return self._reaction

    #-----------------------------------------------------------------------------
    def setResizing(self, resizing: bool):
        self._resizing = resizing

    #-----------------------------------------------------------------------------
    def resizing(self) -> bool:
        return self._resizing
