# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import logging
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.CRITICAL)

import sys
#import typing

from PyQt5.QtWidgets import  QApplication

from FlowView import *
from FlowScene import *
from DataModelRegistry import *

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
