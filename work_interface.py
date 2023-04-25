# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

# coding:utf-8
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAction
from qfluentwidgets import RoundMenu, PushButton
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter)

                            
from ..common.icon import Icon
from ..common.config import cfg, FEEDBACK_URL, HELP_URL, EXAMPLE_URL
from ..common.style_sheet import StyleSheet

from .gallery_interface import GalleryInterface
from ..common.translator import Translator

from .create_logic import ImageViewer

class GalleryInterface_X(ScrollArea):
    """ Gallery interface """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)

        self.view = QWidget(self)
        # self.toolBar = ToolBar(title, subtitle, self)

        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, self.toolBar.height(), 0, 0)

        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    # def addExampleCard(self, title, widget, sourcePath: str, stretch=0):
    #     card = ExampleCard(title, widget, sourcePath, stretch, self.view)
    #     self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
    #     return card

    def addWorkSpace(self, title):
        card = ImageViewer()
        # card = ExampleCard(title, widget, sourcePath, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
        # card.resize(card.width(), card.height())
        # self.card.resize(self.width(), self.height())

        return card

    # def scrollToCard(self, index: int):
    #     """ scroll to example card """
    #     w = self.vBoxLayout.itemAt(index).widget()
    #     self.verticalScrollBar().setValue(w.y())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        print("111")
        # self.toolBar.resize(self.width(), self.toolBar.height())


class WorkInterface(GalleryInterface_X):
    """ Menu interface """

    def __init__(self, parent=None):

        t = Translator()

        super().__init__(
            title=t.menus,
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )

        self.addWorkSpace('test')

        # button = PushButton(self.tr('Show menu'))
        # button.clicked.connect(lambda: self.createMenu(
        #     button.mapToGlobal(QPoint()) + QPoint(button.width()+5, -100)))

        # self.addExampleCard(
        #     self.tr('Rounded corners menu'),
        #     button,
        #     'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/demo.py'
        # )



    # def createMenu(self, pos):
    #     menu = RoundMenu(parent=self)

    #     # add actions
    #     menu.addAction(QAction(FIF.COPY.icon(), self.tr('Copy')))
    #     menu.addAction(QAction(FIF.CUT.icon(), self.tr('Cut')))

    #     # add sub menu
    #     submenu = RoundMenu(self.tr("Add to"), self)
    #     submenu.setIcon(FIF.ADD.icon())
    #     submenu.addActions([
    #         QAction(FIF.VIDEO.icon(), self.tr('Video')),
    #         QAction(FIF.MUSIC.icon(), self.tr('Music')),
    #     ])
    #     menu.addMenu(submenu)

    #     # add actions
    #     menu.addActions([
    #         QAction(FIF.PASTE.icon(), self.tr('Paste')),
    #         QAction(FIF.CANCEL.icon(), self.tr('Undo'))
    #     ])

    #     # add separator
    #     menu.addSeparator()
    #     menu.addAction(QAction(self.tr('Select all')))

    #     # insert actions
    #     menu.insertAction(
    #         menu.menuActions()[-1], QAction(FIF.SETTING.icon(), self.tr('Settings')))
    #     menu.insertActions(
    #         menu.menuActions()[-1],
    #         [
    #             QAction(FIF.HELP.icon(), self.tr('Help')),
    #             QAction(FIF.FEEDBACK.icon(), self.tr('Feedback'))
    #         ]
    #     )

    #     # show menu
    #     menu.exec(pos, ani=True)
