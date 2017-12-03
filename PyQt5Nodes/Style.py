# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from abc import abstractmethod

from PyQt5.QtCore import  *

##----------------------------------------------------------------------------
class Style(object):
    
    def __init__(self):
        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def loadJsonText(self, jsonText: str):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def loadJsonFile(self, fileName: str):

        pass

    #-------------------------------------------------------------------------
    @abstractmethod
    def loadJosnFromByteArray(self, byteArray: QByteArray):

        pass

##----------------------------------------------------------------------------
