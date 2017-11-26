# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from PyQt5.QtWidgets import  *
from PyQt5.QtCore import  QFile, QIODevice,  QByteArray,  QJsonDocument,  QJsonValue
from PyQt5.QtGui import  QColor

#from resource import *

##----------------------------------------------------------------------------
class FlowViewStyle(object):
    
    BackgroundColor = QColor()
    FineGridColor = QColor()
    CoarseGridColor = QColor()
    
    def __init__(self,  jsonFilePath: str = "./DefaultStyle.json"):
        
            self.loadJsonFile(jsonFilePath)
        
    #-------------------------------------------------------------------------
    def loadJsonFile(self,  styleFile: str):
        
        self.jsonFile = QFile(styleFile)
        
        if(not self.jsonFile.open(QIODevice.ReadOnly)):
            qWarning("Couldn't open file: {}".format(styleFile))
            return
        
        self.loadJsonFromByteArray(self.jsonFile.readAll())
        
    #-------------------------------------------------------------------------
    def setStyle(self,  jsonText: str):
        self.style = FlowViewStyle(jsonText)
        
        self.StyleCollection.setFlowViewStyle(style)
        
    #-------------------------------------------------------------------------
    def loadJsonFromByteArray(self,  byteArray: QByteArray):
        
        json = QJsonDocument(QJsonDocument.fromJson(byteArray))
        
        topLevelObject = json.object()
        
        nodeStyleValues = topLevelObject["FlowViewStyle"]
        
        obj = nodeStyleValues.toObject()

        self.BackgroundColor = self.flowViewStyleReadColor(obj,  "BackgroundColor")
        self.FineGridColor =self.flowViewStyleReadColor(obj,  "FineGridColor")
        self.CoarseGridColor = self.flowViewStyleReadColor(obj,  "CoarseGridColor")

    #-------------------------------------------------------------------------
    def flowViewStyleCheckUndefinedValue(self,  v, variable):
        
        if(type(v) == QJsonValue.Undefined or 
           type(v) == QJsonValue.Null):
            qWarning("Undefined value for parameter: ", variable)
    
    #-------------------------------------------------------------------------
    def flowViewStyleReadColor(self,  values,  variable) -> QColor:
        
        valuesRef = values[variable]
        
        self.flowViewStyleCheckUndefinedValue(valuesRef, variable)

        if(valuesRef.isArray()):

            colorArray = valuesRef.toArray();
            rgb = []
            
            for it in colorArray :
                rgb.append(it.toDouble())
            
            return QColor(rgb[0], rgb[1], rgb[2])
        else:
            return QColor(valueRef.toString())
            
    #-------------------------------------------------------------------------
    def loadJsonText(self,  jsonText: str):
        
        self.loadJsonFromByteArray(jsonText)
         
##----------------------------------------------------------------------------
