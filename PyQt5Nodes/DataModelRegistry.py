# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5Nodes.NodeDataModel import *
#from NodeData import *

class DataModelRegistry(object):
    def __init__(self):
        self._registeredModelsCategory = dict()
        self._registeredModels = dict()
        self._categories = set()
        self._registeredTypeConverters = dict()

#-----------------------------------------------------------------------------
    def create(self, modelName: str) -> NodeDataModel:
        if modelName in self._registeredModels:
            it = self._registeredModels[modelName]
            return it.clone()

        return None

#-----------------------------------------------------------------------------
    def registeredModels(self):
        return self._registeredModels

#-----------------------------------------------------------------------------
    def registeredModelsCategoryAssociation(self):
        return self._registeredModelsCategory

#-----------------------------------------------------------------------------
    def categories(self):
        return self._categories

#-----------------------------------------------------------------------------
    def getTypeConverter(self, sourceTypeId: str, destTypeId: str) -> NodeDataModel:
        typeConverterKey = sourceTypeId
        typeConverterValue = destTypeId

        if(typeConverterKey in self._registeredTypeConverters and
                typeConverterValue == self._registeredTypeConverters[typeConverterKey]):
            return converter(typeConverterKey).Model.clone()

        return None

#-----------------------------------------------------------------------------
    def registerModel(self,  uniqueModel=None, TypeConverter=False,  category="Nodes"):
        if(not isinstance(uniqueModel, NodeDataModel)):
            print("Must pass a subclass of NodeDataModel to registerModel")

        name = uniqueModel.name()

        if(not name in self._registeredModels):
            self._registeredModels[name] = uniqueModel
            self._categories.add(category)
            self._registeredModelsCategory[name] = category

        if(TypeConverter):
            registeredModelRef = self._registeredModels[name]

            # Type converter node should have exactly one input and output
            #   ports, if thats not the case, we skip the registration.
            #If the input and output type is the same, we also skip
            #   registration, because thats not a typecast node.
            if(registeredModelRef.nPorts(PortType.In) != 1 or
                    registeredModelRef.nPorts(PortType.Out) != 1 or
                    registeredModelRef.dataType(PortType.In, 0).id ==
                    registeredModelRef.dataType(PortType.Out, 0).id):
                return

            converter = TypeConverterItem()
            converter.Model = registeredModelRef.clone()
            converter.SourceType = converter.Model.dataType(PortType.In, 0)
            converter.DestinationType = converter.Model.dataType(PortType.Out, 0)

            typeConverterKey = [converter.SourceType.id,
                                 converter.DestinationType.id]

            self._registeredTypeConverters[typeConverterKey] = converter

    #-----------------------------------------------------------------------------
    #def registerModelCatMod

##-----------------------------------------------------------------------------
class TypeConverterItem(object):
    Model = NodeDataModel
    SourceType = NodeDataType
    DestinationType = NodeDataType








