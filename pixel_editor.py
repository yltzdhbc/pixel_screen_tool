# coding:utf-8
import sys

from PyQt5.QtCore import QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QPainter, QPixmap, QWheelEvent, QMouseEvent, QBrush, QPen
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView, QGraphicsEllipseItem)
import numpy as np
import os

TOTAL_LED_NUM = 16*16

class RGB_ITEM(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__()
        self.color = Qt.black
        self.seq = 0

    def set_seq(self, seq):
        self.seq = seq

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print("mousePressEvent", self.seq, self.isSelected())

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print("mouseDoubleClickEvent", self.seq)
        if self.color == Qt.black:
            self.color = Qt.green
            self.setPen(QPen(Qt.green))
        else:
            self.color = Qt.black
            self.setPen(QPen(Qt.black))


class PixelEditor(QGraphicsView):
    """ 图片查看器 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.zoomInTimes = 0
        self.maxZoomInTimes = 200

        # 创建场景
        self.graphicsScene = QGraphicsScene()

        # 图片
        self.pixmap = QPixmap(r'test.jpeg')
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)

        # 从文件中读取数组
        self.xy_buff = np.load("screen_layout_rec16x16.npy")

        # 初始化小部件
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.resize(1200, 1200)

        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 以鼠标所在位置为锚点进行缩放
        self.setTransformationAnchor(self.AnchorUnderMouse)

        # 平滑缩放
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

        objs = list()
        for i in range(TOTAL_LED_NUM):
            objs.append(RGB_ITEM())

        for i in range(TOTAL_LED_NUM):
            objs[i].set_seq(i)
            objs[i].setRect(0, 0, 5, 5)
            objs[i].setPos(self.xy_buff[i][0], self.xy_buff[i][1])
            self.graphicsScene.addItem(objs[i])

        # for item in self.graphicsScene.items():
        #     item.setFlag(QGraphicsItem.ItemIsFocusable, False)
            # item.setFlag(QGraphicsItem.ItemIsMovable)
            # item.setFlag(QGraphicsItem.ItemIsSelectable)

        # 设置场景
        # self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)

    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     print("mouseDoubleClickEvent")

    def wheelEvent(self, e: QWheelEvent):
        """ 滚动鼠标滚轮缩放图片 """
        if e.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def resizeEvent(self, e):
        """ 缩放图片 """
        super().resizeEvent(e)

        if self.zoomInTimes > 0:
            return

        # 调整图片大小
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()

    def setImage(self, imagePath: str):
        """ 设置显示的图片 """
        self.resetTransform()

        # 刷新图片
        self.pixmap = QPixmap(imagePath)
        self.pixmapItem.setPixmap(self.pixmap)

        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)

    def resetTransform(self):
        """ 重置变换 """
        super().resetTransform()
        self.zoomInTimes = 0
        self.__setDragEnabled(False)

    def __isEnableDrag(self):
        # """ 根据图片的尺寸决定是否启动拖拽功能 """
        # v = self.verticalScrollBar().maximum() > 0
        # h = self.horizontalScrollBar().maximum() > 0
        # return v or h
        return True

    def __setDragEnabled(self, isEnabled: bool):
        """ 设置拖拽是否启动 """
        self.setDragMode(
            self.ScrollHandDrag if isEnabled else self.NoDrag)

    def __getScaleRatio(self):
        """ 获取显示的图像和原始图像的缩放比例 """
        if self.pixmap.isNull():
            return 1

        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width()/pw)
        rh = min(1, self.height()/ph)
        return min(rw, rh)

    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        """ 缩放场景使其适应窗口大小 """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio()*self.pixmap.size()
        self.zoomInTimes = 0

    def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 放大图像 """
        if self.zoomInTimes == self.maxZoomInTimes:
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 缩小图像 """
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes -= 1

        # 原始图像的大小
        pw = self.pixmap.width()
        ph = self.pixmap.height()

        # 实际显示的图像宽度
        w = self.displayedImageSize.width()*1.1**self.zoomInTimes
        h = self.displayedImageSize.height()*1.1**self.zoomInTimes

        if pw > self.width() or ph > self.height():
            # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1/1.1, 1/1.1)
        else:
            # 在窗口尺寸大于图像时不允许缩小的比原始图像小
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1/1.1, 1/1.1)

        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)


# if __name__ == '__main__':
#     # 从文件中读取数组
#     x_buff = np.load("x_buff.npy")
#     y_buff = np.load("y_buff.npy")

#     app = QApplication(sys.argv)
#     w = ImageViewer()
#     w.show()
#     sys.exit(app.exec_())
