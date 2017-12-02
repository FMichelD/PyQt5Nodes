# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from math import floor

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import  *


from FlowScene import *
from StyleCollection import *

class FlowView(QGraphicsView):

    def __init__(self, scene: FlowScene=None,  parent: QWidget=None) :
        super(QGraphicsView, self).__init__(parent)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)

        self.flowViewStyle = StyleCollection.flowViewStyle()

        self.setBackgroundBrush(self.flowViewStyle.BackgroundColor)

        #self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate);
        #self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate);
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse);

        self.setCacheMode(QGraphicsView.CacheBackground);

        #self.setViewport(new QGLWidget(QGLFormat(QGL::SampleBuffers)));

        if(scene):
            self.setScene(scene)
            
        """ setup actions """
        self.__clearSelectionAction = QAction(("Clear Selection"), self)
        self.__clearSelectionAction.setShortcut(Qt.Key_Escape)
        self.__clearSelectionAction.triggered.connect(self._scene.clearSelection)
        self.addAction(self.__clearSelectionAction);

        self._deleteSelectionAction = QAction("Delete Selection",self)
        self._deleteSelectionAction.setShortcut(Qt.Key_Delete)
        self._deleteSelectionAction.triggered.connect(self.deleteSelectedNodes)
        self.addAction(self._deleteSelectionAction)
    
    #-------------------------------------------------------------------------
    def clearSelectionAction(self) -> QAction:
        return _clearSelectionAction

    #-------------------------------------------------------------------------
    def deleteSelectionAction(self) -> QAction:
        return _deleteSelectionAction

    #--------------------------------------------------------------------------
    def setScene(self, scene: FlowScene):
        self._scene = scene
        QGraphicsView.setScene(self, self._scene)
        
    #--------------------------------------------------------------------------
    def mousePressEvent(self,  event: QMouseEvent):
        QGraphicsView.mousePressEvent(self, event);

        if(event.button() == Qt.LeftButton):
            self._clickPos = self.mapToScene(event.pos())

    #--------------------------------------------------------------------------
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        QGraphicsView.mouseMoveEvent(self, event);

        if(self._scene.mouseGrabberItem() == None and event.buttons() == Qt.LeftButton):
            if( not(event.modifiers() == Qt.ShiftModifier)):
                difference = self._clickPos - self.mapToScene(event.pos())
                self.setSceneRect(self.sceneRect().translated(difference.x(), difference.y()));

    #-------------------------------------------------------------------------
    def contextMenuEvent(self, event: QContextMenuEvent):

        self.modelMenu = QMenu(self)

        self.skipText = "skip me"

        txtBox = QLineEdit(self.modelMenu)
        txtBox.setPlaceholderText("Filter")
        txtBox.setClearButtonEnabled(True)

        txtBoxAction = QWidgetAction(self.modelMenu)
        txtBoxAction.setDefaultWidget(txtBox)

        self.modelMenu.addAction(txtBoxAction)

        treeView = QTreeWidget(self.modelMenu)
        #treeView.header().close()

        treeViewAction = QWidgetAction(self.modelMenu)
        treeViewAction.setDefaultWidget(treeView)

        self.modelMenu.addAction(treeViewAction)

        self.topLevelItems = dict()
        for cat in self._scene.registry().categories():
            item = QTreeWidgetItem(treeView)
            item.setText(0, cat)
            item.setData(0, Qt.UserRole, self.skipText)
            self.topLevelItems[cat] = item

        registeredModel = self._scene.registry().registeredModelsCategoryAssociation()
        for assoc in registeredModel:
            parent = self.topLevelItems[registeredModel[assoc]]
            item = QTreeWidgetItem(parent)
            item.setText(0, assoc);
            item.setData(0, Qt.UserRole, assoc)

        treeView.expandAll()

        #---------------------------------------------------------------------
        def insertItemAsNode(item: QTreeWidgetItem, column: int):

            self.modelMenu.close()

            modelName = item.data(0, Qt.UserRole)

            if(modelName == self.skipText):
                return

            typeNode = self._scene.registry().create(modelName)

            if(not typeNode is None):
                node = self._scene.createNode(typeNode)

                pos = event.pos()

                posView= self.mapToScene(pos)

                node.nodeGraphicsObject().setPos(posView)
            else:
                qDebug() << "Model not found"

        #---------------------------------------------------------------------

        treeView.itemActivated.connect(insertItemAsNode)

        txtBox.textChanged.connect(self.filtering)

        txtBox.setFocus()

        self.modelMenu.exec(event.globalPos())

    #-------------------------------------------------------------------------
    def filtering(self, text: str):

        for topLvlItem in self.topLevelItems:
            for i in range(0, topLvlItem.childCount()):
                child = topLvlItem.child(i)

                modelName = child.data(0, Qt.UserRole)

                if(modelName.contains(text, Qt.CaseInsensitive)):
                    child.setHidden(False)
                else:
                    child.setHidden(True)

    #-------------------------------------------------------------------------
    def wheelEvent(self, event: QWheelEvent):

        delta = event.angleDelta()

        if(delta.y() == 0):
            event.ignore()
            return

        d = delta.y() / abs(delta.y())

        if(d > 0.0):
            self.scaleUp()
        else:
            self.scaleDown()

    #-------------------------------------------------------------------------
    def keyPressEvent(self, event: QKeyEvent):

        if(event.key() == Qt.Key_Shift):

            self.setDragMode(QGraphicsView.RubberBandDrag)

        QGraphicsView.keyPressEvent(self, event)

    #-------------------------------------------------------------------------
    def keyReleaseEvent(self, event: QKeyEvent):

        if(event.key() == Qt.Key_Shift):

            self.setDragMode(QGraphicsView.ScrollHandDrag)

        QGraphicsView.keyReleaseEvent(self, event)

    #-------------------------------------------------------------------------
    def drawBackground(self, painter: QPainter, r: QRectF):

        QGraphicsView.drawBackground(self, painter, r)

        flowViewStyle = StyleCollection.flowViewStyle()
        bBrush = self.backgroundBrush()

        painter.fillRect(r,  bBrush)

        pen = QPen(flowViewStyle.FineGridColor)
        pen.setWidth(3)
        painter.setPen(pen)
        self.drawGrid(200,  painter)

        pen = QPen(flowViewStyle.CoarseGridColor, 1.0)
        pen.setWidth(0)
        painter.setPen(pen)
        self.drawGrid(20, painter)

    #-------------------------------------------------------------------------
    def  drawGrid (self,  gridStep: int,  painter: QPainter):

            windowRect = self.rect()
            tl = self.mapToScene(windowRect.topLeft())
            br = self.mapToScene(windowRect.bottomRight())

            left   = floor(tl.x() / gridStep - 0.5);
            right  = floor(br.x() / gridStep + 1.0);
            bottom = floor(tl.y() / gridStep - 0.5);
            top    = floor (br.y() / gridStep + 1.0);

            #Vertical lines
            for xi in range(int(left), int(right) + 1):
                line = QLineF(xi * gridStep, bottom * gridStep,
                            xi * gridStep, top * gridStep )
                painter.drawLine(line)

            #Horizontal lines
            for yi in range(int(bottom), int(top) + 1):
                line = QLineF(left * gridStep, yi * gridStep,
                            right * gridStep, yi * gridStep)
                painter.drawLine(line)

    #-------------------------------------------------------------------------
    def showEvent(self, event: QShowEvent):
        self._scene.setSceneRect(self.sceneRect())
        QGraphicsView.showEvent(self, event);

    #-------------------------------------------------------------------------
    def scene(self):
        return self._secne

    #-------------------------------------------------------------------------
    #Slots
    @pyqtSlot()
    def scaleUp(self):
        step = 1.2
        factor = step**1.0

        t = self.transform()

        if(t.m11() > 2.0):
            return

        self.scale(factor, factor)

    @pyqtSlot()
    def scaleDown(self):
        step = 1.2
        factor = step**(-1.0)

        t = self.transform()

        if(t.m11() < 0.3):
            return

        self.scale(factor, factor)

    @pyqtSlot()
    def deleteSelectedNodes(self):
        # delete the nodes, this will delete many of the connections
        for item in self._scene.selectedItems():
            if(isinstance(item,  NodeGraphicsObject)):
                self._scene.removeNode(item.node())

            if(isinstance(item, ConnectionGraphicsObject)):
                self._scene.deleteConnection(item.connection())

##############################################################################

