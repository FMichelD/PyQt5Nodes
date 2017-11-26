# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from random import seed,  randrange

from PyQt5.QtGui import  *
#from DataModelRegistry import *

from Style import *
#from StyleCollection import *

##----------------------------------------------------------------------------
class ConnectionStyle(Style):

    def __init__(self, jsonText: str="./DefaultStyle.json"):        
        #initResoureces()
        self.loadJsonFile(jsonText)

    #-------------------------------------------------------------------------
    def setConnectionSyle(self, jsonText: str):
        self.style = ConnectionStyle(jsonText)
              
#        StyleCollection.setConnectionSyle(style)

    #-------------------------------------------------------------------------
    def ConnectionStyleCheckUndefinedValue(self, v: dict, variable):
        
        if(v.type() == QJsonValue.Undefined or v.type() == QJsonValue.Null):

            qWarning("Undefined value for parameter: {}".format(variable))

    #-------------------------------------------------------------------------
    def ConnectionValuesExists(self, v):

        if(v.type() != QJsonValue.Undefined and v.type() != QJsonValue.Null):        

            return True

    #-------------------------------------------------------------------------
    def ConnectionStyleReadColor(self, values, variable):

        valuesRef = values[variable]

        self.ConnectionStyleCheckUndefinedValue(valuesRef, variable)

        if(self.ConnectionValuesExists(valuesRef)):
        
            if(valuesRef.isArray()):

                colorArray = valuesRef.toArray();

                rgb = []
                
                for it in colorArray :
                    rgb.append(it.toDouble())
                
                return QColor(rgb[0], rgb[1], rgb[2])
            else:
                return QColor(valuesRef.toString())

    #-------------------------------------------------------------------------
    def ConnectionStyleReadFloat(self, values, variable):

        valuesRef = values[variable]

        self.ConnectionStyleCheckUndefinedValue(valuesRef, variable)

        return valuesRef.toDouble()

    #-------------------------------------------------------------------------
    def ConnectionStyleReadBool(self, values, variable):

        valuesRef = values[variable]

        self.ConnectionStyleCheckUndefinedValue(valuesRef, variable)

        if(self.ConnectionValuesExists(valuesRef)):

            return bool(valuesRef)

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

        ConnectionStyleValues = topLevelObject["ConnectionStyle"]

        obj = ConnectionStyleValues.toObject()

        self.ConstructionColor   = self.ConnectionStyleReadColor(obj, "ConstructionColor")
        self.NormalColor = self.ConnectionStyleReadColor(obj, "NormalColor")
        self.SelectedColor = self.ConnectionStyleReadColor(obj, "SelectedColor")
        self.SelectedHaloColor = self.ConnectionStyleReadColor(obj, "SelectedHaloColor")
        self.HoveredColor = self.ConnectionStyleReadColor(obj, "HoveredColor")

        self.LineWidth = self.ConnectionStyleReadFloat(obj, "LineWidth")
        self.ConstructionLineWidth = self.ConnectionStyleReadFloat(obj, "ConstructionLineWidth")
        self.PointDiameter = self.ConnectionStyleReadFloat(obj, "PointDiameter")

        self.UseDataDefinedColors = self.ConnectionStyleReadBool(obj, "UseDataDefinedColors")

    #-------------------------------------------------------------------------
    def constructionColor(self):

        return self.ConstructionColor

    #-------------------------------------------------------------------------
    def normalColor(self, typeId=None):

        if(typeId is None):

            return self.NormalColor

        else:
            
            seed(typeId)
            
            hue = randrange(359) 

            sat = randrange(128,  255)

            return QColor.fromHsl(hue, sat, 160)

    #-------------------------------------------------------------------------
    def selectedColor(self):
        return self.SelectedColor      

    #-------------------------------------------------------------------------
    def selectedHaloColor(self):
        return self.SelectedHaloColor

    #-------------------------------------------------------------------------
    def hoveredColor(self):
        return self.HoveredColor

    #-------------------------------------------------------------------------
    def lineWidth(self):
        return self.LineWidth

    #-------------------------------------------------------------------------
    def constructionLineWidth(self):        
        return self.ConstructionLineWidth

    #-------------------------------------------------------------------------
    def pointDiameter(self):

        return self.PointDiameter

    #-------------------------------------------------------------------------
    def useDataDefinedColors(self):
        
        return self.UseDataDefinedColors

##----------------------------------------------------------------------------
