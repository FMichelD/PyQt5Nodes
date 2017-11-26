# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import inspect
import sys

from collections import namedtuple

from Node import *
from Connection import *
from DataModelRegistry import *
from NodeDataModel import *


# /// Class performs various operations on the Node and Connection pair.
# /// An instance should be created on the stack and destroyed when
# /// the operation is completed
class NodeConnectionInteraction(object):
    
    def __init__(self, node, connection, scene):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print("NodeConnectionInteraction.py: __init__(...)")
#        print('calleed by:', calframe[1][3])
#        print('on:', calframe[1][1])
        
        super().__init__()

        self._node = node

        self._connection = connection

        self._scene = scene

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        #print('\n\ncaller name:', calframe[1][3])
        #print('on:', calframe[1][1])
        #print('\n\n')
    #-------------------------------------------------------------------------
    # /// Can connect when following conditions are met:
    # /// 1) Connection 'requires' a port
    # /// 2) Connection's vacant end is above the node port
    # /// 3) Node port is vacant
    # /// 4) Connection type equals node port type, or there is a 
    #       registered type conversion that can translate between the two
    def canConnect(self, portIndex, typeConsverionNeeded, converterModel):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print('\n\ncaller name:', calframe[1][3])
#        print('on:', calframe[1][1])
#        print('\n\n')

        # typeConsverionNeeded = False
        canConnectRet = namedtuple('CanConnectRet', 'canConnect, needConvesion')
        
        requiredPort = self.connectionRequiredPort()

        # 1) Connection requires a port
        if(requiredPort == PortType.No_One):

            canConnectRet = canConnectRet(canConnect = False, needConvesion = False)

            return canConnectRet

        # 2) connection point is on top of the node port
        connectionPoint = self.connectionEndScenePosition(requiredPort)

        portIndex = self.nodePortIndexUnderScenePoint(requiredPort, connectionPoint)

        if(portIndex == INVALID):

            canConnectRet = canConnectRet(canConnect = False, needConvesion = False)

            return canConnectRet

        # 3) Node port is vacant
        # port should be empty
        if(not self.nodePortIsEmpty(requiredPort, portIndex)):

            canConnectRet = canConnectRet(canConnect = False, needConvesion = False)

            return canConnectRet

        # 4) Connection type equals node port type, or there is a 
        #       registered type conversion that can translate between the two
        connectionDataType = self._connection.dataType()

        modelTarget = self._node.nodeDataModel()

        candidateNodeDataType = modelTarget.dataType(requiredPort, portIndex)

        if(connectionDataType.id != candidateNodeDataType.id):

            if(requiredPort == PortType.In):

                converterModel = self._scene.registry().getTypeConverter(
                                                connectionDataType.id, 
                                                candidateNodeDataType.id)
                if(not converterModel is None):

                    canConnectRet = canConnectRet(canConnect = True,
                                                 needConvesion = True)
                
                    return canConnectRet

            converterModel = self._scene.registry().getTypeConverter(
                                                candidateNodeDataType.id, 
                                                connectionDataType.id)

            if(not converterModel is None):

                canConnectRet = canConnectRet(canConnect = True,
                                             needConvesion = True)

                return canConnectRet

        canConnectRet = canConnectRet(canConnect = True, needConvesion = False)

        return canConnectRet


    #-------------------------------------------------------------------------
    # /// 1)   Check conditions from 'canConnect'
    # /// 1.5) If the connection is possible but a type conversion is needed, 
    #           add a converter node to the scene, and connect it properly
    # /// 2)   Assign node to required port in Connection
    # /// 3)   Assign Connection to empty port in NodeState
    # /// 4)   Adjust Connection geometry
    # /// 5)   Poke model to initiate data transfer
    def tryConnect(self):


        # 1) Check conditions from 'canConnect'
        portIndex = INVALID

        typeConsverionNeeded = False

        typeConveterModel = NodeDataModel()

        canConnect, typeConsverionNeeded = self.canConnect(portIndex, 
                                                typeConsverionNeeded, 
                                                typeConveterModel)

        if(not canConnect):

            return False

        # 1.5) If the connection is possible but a type conversion is
        #        needed, add a converter node to the scene, and connect it properly  
        if(typeConsverionNeeded):

            # Determinig port types
            requiredPort = self.connectionRequiredPort()

            if(requiredPort == PortType.Out):

                connectedPort = PortType.In

            elif(requiredPort == PortType.Out):

                connectedPort = PortType.Out

            else:

                Q_UNREACHABLE()

            # Get the node and port from where the connection starts
            outNode = self._connection.getNode(connectedPort)
            outNodePortIndex = self._connection.getPortIndex(connectedPort)

            # Creating the converter node
            converterNode = self._scene.createNode(typeConveterModel)           

            # Calculate and set the converter node's position
            converterNodePos = NodeGeometry.calculateNodePositionBetweenNodePorts(
                            portIndex, requiredPort, self._node, outNodePortIndex, 
                            connectedPort, converterNode)

            converterNode.nodeGraphicsObject().setPos(converterNodePos)

            # Connecting the converter node to the two nodes trhat
            #    originally supposed to be connected.
            # The connection order is different based on if the users
            #    connection was started from an input port, or an output port.
            if(requiredPort == PortType.In):

                self._scene.createConnection(converterNode, 0, outNode, outNodePortIndex)
                self._scene.createConnection(self._node, portIndex, converterNode, 0)

            else:

                self._scene.createConnection(converterNode, 0, self._node, portIndex)
                self._scene.createConnection(outNode, outNodePortIndex, converterNodePos, 0)
            
            # Delete the users connection, we already replaced it
            self._scene.deleteConnection(self._connection)

            return True

   
        # 2) Assign node to required port in Connection
        requiredPort = self.connectionRequiredPort()

        self._node.nodeState().setConnection(requiredPort, portIndex, self._connection)

        # 3) Assign Connection to empty port in NodeState
        # The port is not longer required after this function
        self._connection.setNodeToPort(self._node, requiredPort, portIndex)

        # 4) Adjust Connection geometry

        self._node.nodeGraphicsObject().moveConnections()

        # 5) Poke model to intiate data transfer

        outNode = self._connection.getNode(PortType.Out)

        if(outNode):

            outNodePortIndex = self._connection.getPortIndex(PortType.Out)

            outNode.onDataUpdated(outNodePortIndex)

        return True

    #-------------------------------------------------------------------------
    # /// 1) Node and Connection should be already connected
    # /// 2) If so, clear Connection entry in the NodeState
    # /// 3) Propagate invalid data to IN node
    # /// 4) Set Connection end to 'requiring a port'
    def disconnect(self, portToDisconnect):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        print("NodeConnectionInteraction.py: disconnect(...)")
#        print('calleed by:', calframe[1][3])
#        print('on:', calframe[1][1])
        
        portIndex = self._connection.getPortIndex(portToDisconnect)

        state = self._node.nodeState()

        # clear pointer to Connection in the NodeState
        state.getEntries(portToDisconnect)[portIndex].clear()

        # 4) Propagate invalid data to IN node
        self._connection.propagateEmptyData()

        # clear Connection side
        self._connection.clearNode(portToDisconnect)

        self._connection.setRequiredPort(portToDisconnect)

        self._connection.getConnectionGraphicsObject().grabMouse()

        return True

    #-------------------------------------------------------------------------
    #------------------ util functions below
    def connectionRequiredPort(self):
#        curframe = inspect.currentframe()
#        calframe = inspect.getouterframes(curframe, 2)
#        #print("\nNodeConnectionInteraction.py:connectionRequiredPort \t")
#        #print('called by:', calframe[1][3])
#        #print('on:', calframe[1][1])
#        #print('\n')
        
        state = self._connection.connectionState()

        return state.requiredPort()

    #-------------------------------------------------------------------------
    def connectionEndScenePosition(self,  portType: PortType):
        
        go = self._connection.getConnectionGraphicsObject()

        geometry = self._connection.connectionGeometry()

        endPoint = geometry.getEndPoint(portType)

        return go.mapToScene(endPoint)

    #-------------------------------------------------------------------------
    def nodePortScenePosition(self, portType, portIndex):

        geom = self._node.nodeGeometry()

        p = geom.nodePortScenePosition(portIndex, portType)

        ngo = self._node.nodeGraphicsObject()

        return ngo.sceneTransform().map(p)

    #-------------------------------------------------------------------------
    def nodePortIndexUnderScenePoint(self, portType, scenePoint):

        nodeGeom = self._node.nodeGeometry()

        sceneTransform = self._node.nodeGraphicsObject().sceneTransform()

        portIndex = nodeGeom.checkHitScenePoint(portType, scenePoint, sceneTransform)

        return portIndex

    #-------------------------------------------------------------------------
    def nodePortIsEmpty(self, portType, portIndex):

        nodeState = self._node.nodeState()

        entries = nodeState.getEntries(portType)

        return (portType == PortType.Out) or (not entries[portIndex])
