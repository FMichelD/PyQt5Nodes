# -*- coding: utf-8 -*-
# !/usr/bin/env python3


from PyQt5.QtWidgets import *


#from ConnectionGraphicsObject import *
#from ConnectionPainter import *

##----------------------------------------------------------------------------
class ConnectionBlurEffect(QGraphicsBlurEffect):

    # _object = ConnectionGraphicsObject()

    def __init__(self, cgobject):

        super().__init__()

        self._object = cgobject

    #-------------------------------------------------------------------------
    def draw(self, painter):

        QGraphicsBlurEffect.draw(painter)

        # //ConnectionPainter::paint(painter,
        # //_object->connectionGeometry(),
        # //_object->connectionState());

        # //_item->paint(painter, nullptr, nullptr);
