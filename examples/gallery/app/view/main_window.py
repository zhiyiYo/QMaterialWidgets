# coding: utf-8
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from qmaterialwidgets import (NavigationItemPosition, MaterialWindow, SplashScreen, Theme,
                              setTheme, isDarkTheme, OutlinedToolButton, ToolTipFilter)
from qmaterialwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BasicInputInterface
from .date_time_interface import DateTimeInterface
from .dialog_interface import DialogInterface
from .text_interface import TextInterface
from .status_info_interface import StatusInfoInterface
from .navigation_view_interface import NavigationViewInterface
from .view_interface import ViewInterface
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource


class MainWindow(MaterialWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.basicInputInterface = BasicInputInterface(self)
        self.dateTimeInterface = DateTimeInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.navigationViewInterface = NavigationViewInterface(self)
        self.statusInfoInterface = StatusInfoInterface(self)
        self.textInterface = TextInterface(self)
        self.viewInterface = ViewInterface(self)

        # initialize layout
        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.toggleThemeSignal.connect(self.toggleTheme)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX, t.basicInput, position=pos)
        self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, position=pos)
        self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, position=pos)
        self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, position=pos)
        self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, position=pos)
        self.addSubInterface(self.textInterface, Icon.TEXT, t.text, position=pos)
        self.addSubInterface(self.viewInterface, Icon.GRID, t.view, position=pos)

        self.themeButton = OutlinedToolButton(FIF.QUIET_HOURS, self)
        self.themeButton.setFixedSize(50, 50)
        self.themeButton.setIconSize(QSize(20, 20))
        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton, 500))
        self.themeButton.setToolTip(self.tr('Toggle theme'))
        self.navigationInterface.addWidget(
            'themeButton', self.themeButton, self.toggleTheme, NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(990, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/qmaterialwidgets/images/logo.png'))
        self.setWindowTitle('PySide-Material-Widgets')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(120, 120))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def toggleTheme(self):
        theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        setTheme(theme, save=True)

        if theme == Theme.LIGHT:
            self.themeButton.setIcon(FIF.QUIET_HOURS)
        else:
            self.themeButton.setIcon(FIF.BRIGHTNESS)

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
