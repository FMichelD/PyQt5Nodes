# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import sys
from math import floor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import  *
from PyQt5.QtGui import  *

class myView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drawBackground(self, painter, rect):

        background_brush = QBrush( QColor(63,63,63), Qt.SolidPattern)
        painter.fillRect(rect, background_brush)

        pen = QPen(QColor(46, 84, 255))
        pen.setWidth(5)
        painter.setPen(pen)
#
        line1 = QLineF(0,0,0,100)
        line2 = QLineF(0,100,100,100)
#        line3 = QLineF(100,100,100,0)
#        line4 = QLineF(100,0,0,0)
#        painter.drawLines([line1, line2, line3, line4])

        painter.drawLine(line1)
        
        pfine = QPen(QColor(100, 100, 100))
        pfine.setWidth(5)
        painter.setPen(pfine)
        painter.drawLine(line2)
        
        self.drawGrid(10,  painter)
        
#        p = QPen(flowViewStyle.CoarseGridColor, 1.0)
#        
#        painter.setPen(p)
#        self.drawGrid(15, painter)

    def   drawGrid (self,  gridStep: int,  painter: QPainter):
            windowRect = QRect()
            tl = self.mapToScene(windowRect.topLeft())
            br = self.mapToScene(windowRect.bottomRight())
            
            left   = floor(tl.x() / gridStep - 0.5);
            right  = floor(br.x() / gridStep + 1.0);
            bottom = floor(tl.y() / gridStep - 0.5);
            top    = floor (br.y() / gridStep + 1.0); 
    
#            #Vertical lines
#            for xi in range(int(left), int(right) + 1):
#                line = QLineF(xi * gridStep, bottom * gridStep,
#                            xi * gridStep, top * gridStep )
#                painter.drawLine(line)
        
            #Horizontal lines
            for yi in range(int(bottom), int(top) + 1):
                line = QLineF(left * gridStep, yi * gridStep, 
                            right * gridStep, yi * gridStep)
                painter.drawLine(line)
                
                
if __name__ == '__main__':
    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.addEllipse(0,0,100,100)

    view = myView(scene)
    view.show()
    view.centerOn(50,50)

    app.exec_()
