# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QListWidgetItem, QListWidget, QWidget, QHBoxLayout

from qmaterialwidgets import ListView, setTheme, Theme, ListWidget, ElevatedCardWidget



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")

        self.hBoxLayout = QHBoxLayout(self)
        self.cardWidget = ElevatedCardWidget(self)
        self.cardLayout = QHBoxLayout(self.cardWidget)
        self.listWidget = ListWidget(self.cardWidget)

        # self.listWidget.setAlternatingRowColors(True)

        # self.listWidget.setSelectRightClickedRow(True)

        stands = [
            '白金之星', '绿色法皇', "天堂制造", "绯红之王",
            '银色战车', '疯狂钻石', "壮烈成仁", "败者食尘",
            "黑蚊子多", '杀手皇后', "金属制品", "石之自由",
            "砸瓦鲁多", '钢链手指', "臭氧宝宝", "华丽挚爱",
            "隐者之紫", "黄金体验", "虚无之王", "纸月之王",
            "骇人恶兽", "男子领域", "20世纪男孩", "牙 Act 4",
            "铁球破坏者", "性感手枪", 'D4C • 爱之列车', "天生完美",
            "软又湿", "佩斯利公园", "奇迹于你", "行走的心",
            "护霜旅行者", "十一月雨", "调情圣手", "片刻静候"
        ]
        for stand in stands:
            item = QListWidgetItem(stand)
            # item.setIcon(QIcon(':/qmaterialwidgets/images/logo.png'))
            item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)

        self.hBoxLayout.setContentsMargins(50, 50, 50, 50)
        self.cardLayout.setContentsMargins(0, 8, 0, 8)
        self.hBoxLayout.addWidget(self.cardWidget)
        self.cardLayout.addWidget(self.listWidget)
        self.resize(400, 486)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
