# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtWidgets import  QApplication

import sys
sys.path.insert(0, '../../../PyQt5Nodes/')

from PyQt5Nodes.NodeData import *
from PyQt5Nodes.NodeDataModel import *
from PyQt5Nodes.FlowScene import *
from PyQt5Nodes.FlowView import *
from PyQt5Nodes.ConnectionStyle import *
from PyQt5Nodes.DataModelRegistry import *

from NumberSourceDataModel import *
from NumberDisplayDataModel import *
from AdditionModel import *
from SubtractionModel import *
from MultiplicationModel import *
from DivisionModel import *
from ModuloModel import *
from DecimalToIntegerModel import *
from IntegerToDecimalModel import *


#-------------------------------------------------------------------------------
def registerDataModels() -> DataModelRegistry:

    ret = DataModelRegistry()

    ret.registerModel(NumberSourceDataModel())
    ret.registerModel(NumberDisplayDataModel())

    ret.registerModel(AdditionModel())
#    ret.registerModel(SubtractionModel("Operators"))
#    ret.registerModel(MultiplicationModel("Operators"))
#    ret.registerModel(DivisionModel("Operators"))
#    ret.registerModel(ModuleModel("Operators"))
#
#    ret.registerModel(DecimalToIntegerModel("Type converters"))
#    ret.registerModel(IntegerToDecimalModel("Type converters"))

    return ret

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)

    scene = FlowScene(registerDataModels())

    view = FlowView(scene)
    view.setScene(scene)
    view.setWindowTitle("Node-based flow editor")
    view.resize(800, 600)

    view.show()

    e = app.exec_()
    sys.exit(e)
