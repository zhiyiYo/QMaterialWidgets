# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from qmaterialwidgets import TabWidget, setTheme, Theme, FluentIcon, palette


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet(f"""
            Demo{{background: {palette.surface.name()}}}
            QLabel{{
                font: 20px 'Segoe UI';
                background: transparent;
                border-radius: 8px;
                color: {palette.onSurface.name()}
            }}
        """)
        self.resize(400, 400)

        self.tabWidget = TabWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.videoInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('GitHub Interface', self)

        # add items to pivot
        self.addSubInterface(self.videoInterface, 'videoInterface', 'Bus', FluentIcon.BUS)
        self.addSubInterface(self.albumInterface, 'albumInterface', 'Train', FluentIcon.TRAIN)
        self.addSubInterface(self.artistInterface, 'githubInterface', 'GitHub', FluentIcon.GITHUB)

        self.vBoxLayout.addWidget(self.tabWidget)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.videoInterface)
        self.tabWidget.setCurrentItem(self.videoInterface.objectName())

    def addSubInterface(self, widget: QLabel, objectName, text, icon):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.tabWidget.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
            icon=icon
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.tabWidget.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()