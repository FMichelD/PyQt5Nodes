# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from PyQt5.QtWidgets import  QApplication

import sys
sys.path.insert(0, '/home/fmicheld/Workspace/PyQt/PyQt5Nodes/')

from PyQt5Nodes.FlowView import *
from PyQt5Nodes.FlowScene import *
from PyQt5Nodes.DataModelRegistry import *

from models import *

#-------------------------------------------------------------------------------
def registerDataModels() -> DataModelRegistry:
    
    ret = DataModelRegistry()
    
    ret.registerModel(NaiveDataModel())
    ret.registerModel(Otro())
    
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
