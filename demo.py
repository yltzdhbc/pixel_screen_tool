import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale, QModelIndex
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QListWidgetItem
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor
from Ui_LoginWindow import Ui_Form

from pixel_editor import PixelEditor

class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')

        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        # self.label.setScaledContents(False)
        self.setWindowTitle("flams's pixel tool")
        # self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId())
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: black
            }
        """)



        self.comboBox.addItems(['矩形点阵16x16', '圆形点阵'])
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)
        self.comboBox.move(200, 200)



        # self.listWidget.setAlternatingRowColors(True)

        stands = [
            '设备 | ID:0 | SN:SSXC89933V | 类型: STM32',
            '设备 | ID:1 | SN:SSXC3sf36F | 类型: STM32',
        ]
        for stand in stands:
            item = QListWidgetItem(stand)
            # item.setIcon(QIcon('docs/source/_static/logo.png'))
            # item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)


        # # NOTE: use custom item delegate
        # # self.tabFileView.setItemDelegate(CustomTableItemDelegate(self.tabFileView))

        # self.tabFileView.setWordWrap(False)
        # self.tabFileView.setRowCount(2)
        # self.tabFileView.setColumnCount(2)
        # songInfos = [
        #     ['矩阵16X16', 'screen_layout_rec16x16'],
        #     ['圆环布局', 'screen_layout_ring'],
        # ]
        # songInfos += songInfos
        # for i, songInfo in enumerate(songInfos):
        #     for j in range(2):
        #         self.tabFileView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        # self.tabFileView.verticalHeader().hide()
        # self.tabFileView.setHorizontalHeaderLabels(['布局', '路径'])
        # self.tabFileView.resizeColumnsToContents()
        # # self.tabFileView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # # self.tabFileView.setSortingEnabled(True)



        # self.tabFileView_2.setWordWrap(False)
        # self.tabFileView_2.setRowCount(2)
        # self.tabFileView_2.setColumnCount(2)
        # songInfos = [
        #     ['矩阵16X16', 'screen_layout_rec16x16'],
        #     ['圆环布局', 'screen_layout_ring'],
        # ]
        # songInfos += songInfos
        # for i, songInfo in enumerate(songInfos):
        #     for j in range(2):
        #         self.tabFileView_2.setItem(i, j, QTableWidgetItem(songInfo[j]))

        # self.tabFileView_2.verticalHeader().hide()
        # self.tabFileView_2.setHorizontalHeaderLabels(['布局', '路径'])
        # self.tabFileView_2.resizeColumnsToContents()


        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        # pixmap = QPixmap(":/images/background.jpg").scaled(
        #     self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        # self.label.setPixmap(pixmap)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    # translator = QTranslator()
    # translator.load(QLocale.system(), ":/i18n/qfluentwidgets_")
    # app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec_()