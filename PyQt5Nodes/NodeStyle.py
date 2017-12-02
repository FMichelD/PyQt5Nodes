# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtGui import  *
from PyQt5.QtCore import *

from Style import *
#from StyleCollection import *

##----------------------------------------------------------------------------
class NodeStyle(Style):

    def __init__(self, jsonText: str="./DefaultStyle.json"):
        
        #initResoureces()

        self.loadJsonFile(jsonText)

    #-------------------------------------------------------------------------
    def setNodeSyle(self, jsonText: str):

        self.style = NodeStyle(jsonText)
        
#        StyleCollection.setNodeSyle(style)

    #-------------------------------------------------------------------------
    def nodeStyleCheckUndefinedValue(self, v: dict, variable):
        
        if(v.type() == QJsonValue.Undefined or v.type() == QJsonValue.Null):

            qWarning("Undefined value for parameter: {}".format(variable))

    #-------------------------------------------------------------------------
    def nodeStyleReadColor(self, values, variable):

        valuesRef = values[variable]

        self.nodeStyleCheckUndefinedValue(valuesRef, variable)
        
        if(valuesRef.isArray()):

            colorArray = valuesRef.toArray();

            rgb = []
            
            for it in colorArray :
                rgb.append(it.toDouble())
            
            return QColor(rgb[0], rgb[1], rgb[2])
        else:
            return QColor(valuesRef.toString())

    #-------------------------------------------------------------------------
    def nodeStyleReadFloat(self, values, variable):

        valuesRef = values[variable]

        self.nodeStyleCheckUndefinedValue(valuesRef, variable)
        
        return valuesRef.toDouble()

    #-------------------------------------------------------------------------
    def loadJsonFile(self, styleFile: str):

        file = QFile(styleFile)
        
        if(not file.open(QIODevice.ReadOnly)):

            qWarning("Couldn't open file: {}".format(styleFile))

            return

        self.loadJsonFromByteArray(file.readAll())

    #-------------------------------------------------------------------------
    def loadJsonText(self, jsonText: str):

        self.loadJsonFromByteArray(jsonText)

    #-------------------------------------------------------------------------
    def loadJsonFromByteArray(self, byteArray: QByteArray):

        json = QJsonDocument(QJsonDocument.fromJson(byteArray))

        topLevelObject = json.object()

        nodeStyleValues = topLevelObject["NodeStyle"]

        obj = nodeStyleValues.toObject()

        self.NormalBoundaryColor  = self.nodeStyleReadColor(obj, "NormalBoundaryColor")
        self.SelectedBoundaryColor = self.nodeStyleReadColor(obj, "SelectedBoundaryColor")
        self.GradientColor0 = self.nodeStyleReadColor(obj, "GradientColor0")
        self.GradientColor1 = self.nodeStyleReadColor(obj, "GradientColor1")
        self.GradientColor2 = self.nodeStyleReadColor(obj, "GradientColor2")
        self.GradientColor3 = self.nodeStyleReadColor(obj, "GradientColor3")
        self.ShadowColor = self.nodeStyleReadColor(obj, "ShadowColor")
        self.FontColor = self.nodeStyleReadColor(obj, "FontColor")
        self.FontColorFaded = self.nodeStyleReadColor(obj, "FontColorFaded")
        self.ConnectionPointColor = self.nodeStyleReadColor(obj, "ConnectionPointColor")
        self.FilledConnectionPointColor = self.nodeStyleReadColor(obj, "FilledConnectionPointColor")
        self.WarningColor = self.nodeStyleReadColor(obj, "WarningColor")
        self.ErrorColor = self.nodeStyleReadColor(obj, "ErrorColor")

        self.PenWidth = self.nodeStyleReadFloat(obj, "PenWidth")
        self.HoveredPenWidth = self.nodeStyleReadFloat(obj, "HoveredPenWidth")
        self.ConnectionPointDiameter = self.nodeStyleReadFloat(obj, "ConnectionPointDiameter")

        self.Opacity = self.nodeStyleReadFloat(obj, "Opacity")

##----------------------------------------------------------------------------
