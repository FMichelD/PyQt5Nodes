# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from abc import abstractmethod

from PyQt5.QtCore import QObject, QVariant,  pyqtSignal,  pyqtSlot

##----------------------------------------------------------------------------
class FlowItemInterface(QObject):

    def __init__(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getFlowItemSignature(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getNodeTitle(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getNodeInSignature(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getNodeInNames(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def NodeOutSignatures(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getNodeOutNames(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def setData(self):
        
        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def getData(self):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def clone(self):

        pass

    #-------------------------------------------------------------------------
    #Signals
    outputDataChange = pyqtSignal(str, QVariant)

    #-------------------------------------------------------------------------
    #Slots
    @abstractmethod
    @pyqtSlot()
    def inputDataChanged(inSignature, data):

        pass
    #-------------------------------------------------------------------------

