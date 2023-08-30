# coding:utf-8
import json

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qmaterialwidgets import ScrollArea, isDarkTheme, FluentIcon
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, MaterialIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Material Gallery', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            ':/qmaterialwidgets/images/logo.png',
            self.tr('Getting started'),
            self.tr('An overview of app development options and samples.'),
            HELP_URL
        )

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr(
                'The latest fluent design controls and styles for your applications.'),
            REPO_URL
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('Code samples'),
            self.tr(
                'Find samples that demonstrate specific tasks, features and APIs.'),
            EXAMPLE_URL
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('Send feedback'),
            self.tr('Help us improve PySide-Material-Widgets by providing feedback.'),
            FEEDBACK_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # draw background color
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ load samples """
        # basic input samples
        basicInputView = SampleCardView(
            self.tr("Basic input samples"), self.view)
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/Button.png",
            title="Button",
            content=self.tr(
                "A control that responds to user input and emit clicked signal."),
            routeKey="basicInputInterface",
            index=0
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/Checkbox.png",
            title="CheckBox",
            content=self.tr("A control that a user can select or clear."),
            routeKey="basicInputInterface",
            index=11
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ComboBox.png",
            title="ComboBox",
            content=self.tr(
                "A drop-down list of items a user can select from."),
            routeKey="basicInputInterface",
            index=13
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/DropDownButton.png",
            title="DropDownButton",
            content=self.tr(
                "A button that displays a flyout of choices when clicked."),
            routeKey="basicInputInterface",
            index=17
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/RadioButton.png",
            title="RadioButton",
            content=self.tr(
                "A control that allows a user to select a single option from a group of options."),
            routeKey="basicInputInterface",
            index=22
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/Slider.png",
            title="Slider",
            content=self.tr(
                "A control that lets the user select from a range of values by moving a Thumb control along a track."),
            routeKey="basicInputInterface",
            index=23
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ToggleSwitch.png",
            title="SwitchButton",
            content=self.tr(
                "A switch that can be toggled between 2 states."),
            routeKey="basicInputInterface",
            index=24
        )
        basicInputView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ToggleButton.png",
            title="ToggleButton",
            content=self.tr(
                "A button that can be switched between two states like a CheckBox."),
            routeKey="basicInputInterface",
            index=25
        )
        self.vBoxLayout.addWidget(basicInputView)

        # date time samples
        dateTimeView = SampleCardView(self.tr('Date & time samples'), self.view)
        dateTimeView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/CalendarDatePicker.png",
            title="CalendarPicker",
            content=self.tr("A control that lets a user pick a date value using a calendar."),
            routeKey="dateTimeInterface",
            index=0
        )
        dateTimeView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/TimePicker.png",
            title="TimePicker",
            content=self.tr(
                "A configurable control that lets a user pick a time value."),
            routeKey="dateTimeInterface",
            index=2
        )
        self.vBoxLayout.addWidget(dateTimeView)

        # dialog samples
        dialogView = SampleCardView(self.tr('Dialog samples'), self.view)
        dialogView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ContentDialog.png",
            title="MessageBox",
            content=self.tr("A message dialog with mask."),
            routeKey="dialogInterface",
            index=0
        )
        dialogView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/Flyout.png",
            title="Flyout",
            content=self.tr("Shows contextual information and enables user interaction."),
            routeKey="dialogInterface",
            index=1
        )
        dialogView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/TeachingTip.png",
            title="TeachingTip",
            content=self.tr("A content-rich flyout for guiding users and enabling teaching moments."),
            routeKey="dialogInterface",
            index=3
        )
        self.vBoxLayout.addWidget(dialogView)

        # navigation
        navigationView = SampleCardView(self.tr('Navigation'), self.view)
        navigationView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/Pivot.png",
            title="NavigationBar",
            content=self.tr(
                "Offer a persistent, convenient way to switch between primary destinations in an app."),
            routeKey="navigationViewInterface",
            index=0
        )
        navigationView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/TabView.png",
            title="TabWidget",
            content=self.tr(
                "Presents information from different sources in a tabbed view."),
            routeKey="navigationViewInterface",
            index=1
        )
        self.vBoxLayout.addWidget(navigationView)

        # state info samples
        stateInfoView = SampleCardView(self.tr('Status & info samples'), self.view)
        stateInfoView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ToolTip.png",
            title="ToolTip",
            content=self.tr(
                "Displays information for an element in a pop-up window."),
            routeKey="statusInfoInterface",
            index=0
        )
        stateInfoView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/InfoBadge.png",
            title="InfoBadge",
            content=self.tr(
                "An non-intrusive Ul to display notifications or bring focus to an area."),
            routeKey="statusInfoInterface",
            index=2
        )
        stateInfoView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/InfoBar.png",
            title="InfoBar",
            content=self.tr(
                "An inline message to display app-wide status change information."),
            routeKey="statusInfoInterface",
            index=3
        )
        stateInfoView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ProgressBar.png",
            title="ProgressBar",
            content=self.tr(
                "Shows the apps progress on a task, or that the app is performing ongoing work that doesn't block user interaction."),
            routeKey="statusInfoInterface",
            index=7
        )
        stateInfoView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ProgressRing.png",
            title="ProgressRing",
            content=self.tr(
                "Shows the apps progress on a task, or that the app is performing ongoing work that doesn't block user interaction."),
            routeKey="statusInfoInterface",
            index=9
        )
        self.vBoxLayout.addWidget(stateInfoView)

        # text samples
        textView = SampleCardView(self.tr('Text samples'), self.view)
        textView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/TextBox.png",
            title="LineEdit",
            content=self.tr("A single-line plain text field."),
            routeKey="textInterface",
            index=0
        )
        textView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/RichEditBox.png",
            title="TextEdit",
            content=self.tr(
                "A rich text editing control that supports formatted text, hyperlinks, and other rich content."),
            routeKey="textInterface",
            index=6
        )
        self.vBoxLayout.addWidget(textView)

        # view samples
        collectionView = SampleCardView(self.tr('View samples'), self.view)
        collectionView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/DataGrid.png",
            title="TableView",
            content=self.tr(
                "The DataGrid control provides a flexible way to display a collection of data in rows and columns."),
            routeKey="viewInterface",
            index=0
        )
        collectionView.addSampleCard(
            icon=":/qmaterialwidgets/images/controls/ListView.png",
            title="ListView",
            content=self.tr(
                "A control that presents a collection of items in a vertical list."),
            routeKey="viewInterface",
            index=1
        )
        self.vBoxLayout.addWidget(collectionView)
