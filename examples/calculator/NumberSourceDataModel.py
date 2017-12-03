# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')
from PyQt5Nodes.PortType import *
from PyQt5Nodes.NodeData import *
from PyQt5Nodes.NodeDataModel import *

from DecimalData import *

class NumberSourceDataModel(NodeDataModel):
    def __init__(self):
        super().__init__()
        
        self._number = DecimalData()
        
        self._lineEdit = QLineEdit()
        self._lineEdit.setValidator(QDoubleValidator())
        self._lineEdit.setMaximumSize(self._lineEdit.sizeHint())
        
        self._lineEdit.textChanged.connect(self.onTextEdited)
        
        self._lineEdit.setText("0.0")
        
    #--------------------------------------------------------------------------
    #override
    def caption(self):
        return "Number Source"
    
    def setCaption(self, caption:str):
        self._caption = caption
    #--------------------------------------------------------------------------
    #override
    def captionVisible(self):
        return False
    
    #--------------------------------------------------------------------------
    #override
    def name(self):
        return "NumberSource"
    
    #--------------------------------------------------------------------------
    #override
    def clone(self):
        return NumberSourceDataModel()
    
    #--------------------------------------------------------------------------
    #override
    def save(self):
        modelJson = NodeDataModel.save()
        
        if(self._number):
            modelJson["number"] = str(self._number.number())
        
        return modelJson
    
    #--------------------------------------------------------------------------
    #override
    def restore(self, p:dict):
        v = p["number"]
        
        if(not v.isUndefined()):
            strNum = v.toString()
            
            ok, d = strNum.toDouble()
            
            if(ok):
                self._number = DecimalData(d)
                self._lineEdit.setText(strNum)
            
    #--------------------------------------------------------------------------
    #override
    def nPorts(self, portType:PortType):
        result = 0
        
        if(portType == PortType.In):
            result = 0
        elif(portType == PortType.Out):
            result = 1
        
        return result
        
    #--------------------------------------------------------------------------
    #override
    def dataType(self, portType:PortType, portIndex:PortIndex):
        return DecimalData().type()
        
    #--------------------------------------------------------------------------
    #override
    def outData(self, port:PortIndex):
        return self._number
    
    #--------------------------------------------------------------------------
    #override
    def setInData(self, nodeData:NodeData, portIndex:PortIndex):
        pass
    
    #--------------------------------------------------------------------------
    #override
    def embeddedWidget(self):
        return self._lineEdit
    
    #--------------------------------------------------------------------------
    #slots
    def onTextEdited(self, string:str):
        try:
            number = float(self._lineEdit.text())
            self._number = DecimalData(number)
#            dataUpdate.emit(0)
        except ValueError as e:
            dataInvalidated(0)
            print(e)
        
