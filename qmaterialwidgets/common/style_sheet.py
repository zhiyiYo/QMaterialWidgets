# coding:utf-8
from enum import Enum
from string import Template
from typing import List, Union
import weakref

from PyQt5.QtCore import QFile, QObject, QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

from .config import qconfig, Theme, isDarkTheme
from .color import mixColor
from .material_color.utils.color_utils import argbFromRgb, redFromArgb, greenFromArgb, blueFromArgb
from .material_color.utils.theme_utils import themeFromSourceColor
from .material_color.scheme.scheme import Scheme


class StyleSheetManager(QObject):
    """ Style sheet manager """

    def __init__(self):
        self.widgets = weakref.WeakKeyDictionary()

    def register(self, source, widget: QWidget, reset=True):
        """ register widget to manager

        Parameters
        ----------
        source: str | StyleSheetBase
            qss source, it could be:
            * `str`: qss file path
            * `StyleSheetBase`: style sheet instance

        widget: QWidget
            the widget to set style sheet

        reset: bool
            whether to reset the qss source
        """
        if isinstance(source, str):
            source = StyleSheetFile(source)

        if widget not in self.widgets:
            widget.destroyed.connect(self.deregister)
            widget.installEventFilter(CustomStyleSheetWatcher(widget))
            self.widgets[widget] = StyleSheetCompose([source, CustomStyleSheet(widget)])

        if not reset:
            self.source(widget).add(source)
        else:
            self.widgets[widget] = StyleSheetCompose([source, CustomStyleSheet(widget)])

    def deregister(self, widget: QWidget):
        """ deregister widget from manager """
        if widget not in self.widgets:
            return

        self.widgets.pop(widget)

    def items(self):
        return self.widgets.items()

    def source(self, widget: QWidget):
        """ get the qss source of widget """
        return self.widgets.get(widget, StyleSheetCompose([]))


styleSheetManager = StyleSheetManager()


class QssTemplate(Template):
    """ style sheet template """

    delimiter = '--'


def applyThemeColor(qss: str):
    """ apply theme color to style sheet

    Parameters
    ----------
    qss: str
        the style sheet string to apply theme color, the substituted variable
        should be equal to the value of `ThemeColor` and starts width `--`, i.e `--ThemeColorPrimary`
    """
    template = QssTemplate(qss)
    mappings = {c.value: c.name() for c in ThemeColor._member_map_.values()}
    mappings.update({n: c.name() for n, c in palette.colors().items()})
    return template.safe_substitute(mappings)


class StyleSheetBase:
    """ Style sheet base class """

    def path(self, theme=Theme.AUTO):
        """ get the path of style sheet """
        raise NotImplementedError

    def content(self, theme=Theme.AUTO):
        """ get the content of style sheet """
        return getStyleSheetFromFile(self.path(theme))

    def apply(self, widget: QWidget, theme=Theme.AUTO):
        """ apply style sheet to widget """
        setStyleSheet(widget, self, theme)


class MaterialStyleSheet(StyleSheetBase, Enum):
    """ Material style sheet """

    MENU = "menu"
    BUTTON = "button"
    SLIDER = "slider"
    INFO_BAR = "info_bar"
    SPIN_BOX = "spin_box"
    TOOL_TIP = "tool_tip"
    CHECK_BOX = "check_box"
    COMBO_BOX = "combo_box"
    LINE_EDIT = "line_edit"
    LIST_VIEW = "list_view"
    TREE_VIEW = "tree_view"
    INFO_BADGE = "info_badge"
    TAB_WIDGET = "tab_widget"
    TABLE_VIEW = "table_view"
    MESSAGE_BOX = "message_box"
    TIME_PICKER = "time_picker"
    COLOR_DIALOG = "color_dialog"
    SETTING_CARD = "setting_card"
    TEACHING_TIP = "teaching_tip"
    SWITCH_BUTTON = "switch_button"
    STATE_TOOL_TIP = "state_tool_tip"
    CALENDAR_PICKER = "calendar_picker"
    MATERIAL_WINDOW = "material_window"
    FOLDER_LIST_DIALOG = "folder_list_dialog"
    SETTING_CARD_GROUP = "setting_card_group"
    EXPAND_SETTING_CARD = "expand_setting_card"
    NAVIGATION_INTERFACE = "navigation_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/qmaterialwidgets/qss/{theme.value.lower()}/{self.value}.qss"


class StyleSheetFile(StyleSheetBase):
    """ Style sheet file """

    def __init__(self, path: str):
        super().__init__()
        self.filePath = path

    def path(self, theme=Theme.AUTO):
        return self.filePath


class CustomStyleSheet(StyleSheetBase):
    """ Custom style sheet """

    DARK_QSS_KEY = 'darkCustomQss'
    LIGHT_QSS_KEY = 'lightCustomQss'

    def __init__(self, widget: QWidget) -> None:
        super().__init__()
        self.widget = widget

    def path(self, theme=Theme.AUTO):
        return ''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomStyleSheet):
            return False

        return other.widget is self.widget

    def setCustomStyleSheet(self, lightQss: str, darkQss: str):
        """ set custom style sheet in light and dark theme mode """
        self.setLightStyleSheet(lightQss)
        self.setDarkStyleSheet(darkQss)
        return self

    def setLightStyleSheet(self, qss: str):
        """ set the style sheet in light mode """
        self.widget.setProperty(self.LIGHT_QSS_KEY, qss)
        return self

    def setDarkStyleSheet(self, qss: str):
        """ set the style sheet in dark mode """
        self.widget.setProperty(self.DARK_QSS_KEY, qss)
        return self

    def lightStyleSheet(self) -> str:
        return self.widget.property(self.LIGHT_QSS_KEY) or ''

    def darkStyleSheet(self) -> str:
        return self.widget.property(self.DARK_QSS_KEY) or ''

    def content(self, theme=Theme.AUTO) -> str:
        theme = qconfig.theme if theme == Theme.AUTO else theme

        if theme == Theme.LIGHT:
            return self.lightStyleSheet()

        return self.darkStyleSheet()


class CustomStyleSheetWatcher(QObject):
    """ Custom style sheet watcher """

    def eventFilter(self, obj: QWidget, e: QEvent):
        if e.type() != QEvent.Type.DynamicPropertyChange:
            return super().eventFilter(obj, e)

        name = e.propertyName().data().decode()
        if name in [CustomStyleSheet.LIGHT_QSS_KEY, CustomStyleSheet.DARK_QSS_KEY]:
            addStyleSheet(obj, CustomStyleSheet(obj))

        return super().eventFilter(obj, e)


class StyleSheetCompose(StyleSheetBase):
    """ Style sheet compose """

    def __init__(self, sources: List[StyleSheetBase]):
        super().__init__()
        self.sources = sources

    def content(self, theme=Theme.AUTO):
        return '\n'.join([i.content(theme) for i in self.sources])

    def add(self, source: StyleSheetBase):
        """ add style sheet source """
        if source is self or source in self.sources:
            return

        self.sources.append(source)

    def remove(self, source: StyleSheetBase):
        """ remove style sheet source """
        if source not in self.sources:
            return

        self.sources.remove(source)


def getStyleSheetFromFile(file: Union[str, QFile]):
    """ get style sheet from qss file """
    f = QFile(file)
    f.open(QFile.OpenModeFlag.ReadOnly)
    qss = str(f.readAll(), encoding='utf-8')
    f.close()
    return qss



def getStyleSheet(source: Union[str, StyleSheetBase], theme=Theme.AUTO):
    """ get style sheet

    Parameters
    ----------
    source: str | StyleSheetBase
        qss source, it could be:
          * `str`: qss file path
          * `StyleSheetBase`: style sheet instance

    theme: Theme
        the theme of style sheet
    """
    if isinstance(source, str):
        source = StyleSheetFile(source)

    return applyThemeColor(source.content(theme))


def setStyleSheet(widget: QWidget, source: Union[str, StyleSheetBase], theme=Theme.AUTO, register=True):
    """ set the style sheet of widget

    Parameters
    ----------
    widget: QWidget
        the widget to set style sheet

    source: str | StyleSheetBase
        qss source, it could be:
          * `str`: qss file path
          * `StyleSheetBase`: style sheet instance

    theme: Theme
        the theme of style sheet

    register: bool
        whether to register the widget to the style manager. If `register=True`, the style of
        the widget will be updated automatically when the theme changes
    """
    if register:
        styleSheetManager.register(source, widget)

    widget.setStyleSheet(getStyleSheet(source, theme))


def setCustomStyleSheet(widget: QWidget, lightQss: str, darkQss: str):
    """ set custom style sheet

    Parameters
    ----------
    widget: QWidget
        the widget to add style sheet

    lightQss: str
        style sheet used in light theme mode

    darkQss: str
        style sheet used in light theme mode
    """
    CustomStyleSheet(widget).setCustomStyleSheet(lightQss, darkQss)


def addStyleSheet(widget: QWidget, source: Union[str, StyleSheetBase], theme=Theme.AUTO, register=True):
    """ add style sheet to widget

    Parameters
    ----------
    widget: QWidget
        the widget to set style sheet

    source: str | StyleSheetBase
        qss source, it could be:
          * `str`: qss file path
          * `StyleSheetBase`: style sheet instance

    theme: Theme
        the theme of style sheet

    register: bool
        whether to register the widget to the style manager. If `register=True`, the style of
        the widget will be updated automatically when the theme changes
    """
    if register:
        styleSheetManager.register(source, widget, reset=False)
        qss = styleSheetManager.source(widget).content(theme)
    else:
        qss = widget.styleSheet() + '\n' + getStyleSheet(source, theme)

    if qss.rstrip() != widget.styleSheet().rstrip():
        widget.setStyleSheet(qss)



def updateStyleSheet():
    """ update the style sheet of all fluent widgets """
    removes = []
    for widget, file in styleSheetManager.items():
        try:
            setStyleSheet(widget, file, qconfig.theme)
        except RuntimeError:
            removes.append(widget)

    for widget in removes:
        styleSheetManager.deregister(widget)


def setTheme(theme: Theme, save=False):
    """ set the theme of application

    Parameters
    ----------
    theme: Theme
        theme mode

    save: bool
        whether to save the change to config file
    """
    qconfig.set(qconfig.themeMode, theme, save)
    updateStyleSheet()


class ThemeColor(Enum):
    """ Theme color type """

    PRIMARY = "ThemeColorPrimary"
    DARK_1 = "ThemeColorDark1"
    DARK_2 = "ThemeColorDark2"
    DARK_3 = "ThemeColorDark3"
    LIGHT_1 = "ThemeColorLight1"
    LIGHT_2 = "ThemeColorLight2"
    LIGHT_3 = "ThemeColorLight3"

    def name(self):
        return self.color().name()

    def color(self):
        color = qconfig.get(qconfig.themeColor)  # type:QColor

        # transform color into hsv space
        h, s, v, _ = color.getHsvF()

        if isDarkTheme():
            s *= 0.84
            v = 1
            if self == self.DARK_1:
                v *= 0.9
            elif self == self.DARK_2:
                s *= 0.977
                v *= 0.82
            elif self == self.DARK_3:
                s *= 0.95
                v *= 0.7
            elif self == self.LIGHT_1:
                s *= 0.92
            elif self == self.LIGHT_2:
                s *= 0.78
            elif self == self.LIGHT_3:
                s *= 0.65
        else:
            if self == self.DARK_1:
                v *= 0.75
            elif self == self.DARK_2:
                s *= 1.05
                v *= 0.5
            elif self == self.DARK_3:
                s *= 1.1
                v *= 0.4
            elif self == self.LIGHT_1:
                v *= 1.05
            elif self == self.LIGHT_2:
                s *= 0.75
                v *= 1.05
            elif self == self.LIGHT_3:
                s *= 0.65
                v *= 1.05

        return QColor.fromHsvF(h, min(s, 1), min(v, 1))


def themeColor():
    """ get theme color """
    return palette.primary


def setThemeColor(color, save=False):
    """ set theme color

    Parameters
    ----------
    color: QColor | Qt.GlobalColor | str
        theme color

    save: bool
        whether to save to change to config file
    """
    color = QColor(color)
    qconfig.set(qconfig.themeColor, color, save=save)
    updateStyleSheet()


def toggleTheme(save=False):
    """ toggle the theme of application

    Parameters
    ----------
    save: bool
        whether to save the change to config file
    """
    theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
    setTheme(theme, save)


def qcolorToArgb(color: QColor):
    return argbFromRgb(color.red(), color.green(), color.blue())


def argbToQColor(argb: int):
    return QColor(redFromArgb(argb), greenFromArgb(argb), blueFromArgb(argb))


class Palette(QObject):
    """ Palette """

    def __init__(self, color: QColor):
        super().__init__()
        self.setThemeColor(color)

    def setThemeColor(self, color: QColor):
        self.palette = themeFromSourceColor(qcolorToArgb(color))['schemes']

    @property
    def primary(self):
        return argbToQColor(self.scheme.primary)

    @property
    def onPrimary(self):
        return argbToQColor(self.scheme.onPrimary)

    @property
    def primaryContainer(self):
        return argbToQColor(self.scheme.primaryContainer)

    @property
    def onPrimaryContainer(self):
        return argbToQColor(self.scheme.onPrimaryContainer)

    @property
    def secondary(self):
        return argbToQColor(self.scheme.secondary)

    @property
    def secondaryContainer(self):
        return argbToQColor(self.scheme.secondaryContainer)

    @property
    def onSecondary(self):
        return argbToQColor(self.scheme.onSecondary)

    @property
    def onSecondaryContainer(self):
        return argbToQColor(self.scheme.onSecondaryContainer)

    @property
    def tertiary(self):
        return argbToQColor(self.scheme.tertiary)

    @property
    def onTertiary(self):
        return argbToQColor(self.scheme.onTertiary)

    @property
    def tertiaryContainer(self):
        return argbToQColor(self.scheme.tertiaryContainer)

    @property
    def onTertiaryContainer(self):
        return argbToQColor(self.scheme.onTertiaryContainer)

    @property
    def error(self):
        return argbToQColor(self.scheme.error)

    @property
    def onError(self):
        return argbToQColor(self.scheme.onError)

    @property
    def errorContainer(self):
        return argbToQColor(self.scheme.errorContainer)

    @property
    def onErrorContainer(self):
        return argbToQColor(self.scheme.onErrorContainer)

    @property
    def background(self):
        return argbToQColor(self.scheme.background)

    @property
    def onBackground(self):
        return argbToQColor(self.scheme.onBackground)

    @property
    def surface(self):
        return argbToQColor(self.scheme.surface)

    @property
    def onSurface(self):
        return argbToQColor(self.scheme.onSurface)

    @property
    def surfaceContainer(self):
        return argbToQColor(self.scheme.surfaceContainer)

    @property
    def surfaceContainerLow(self):
        return argbToQColor(self.scheme.surfaceContainerLow)

    @property
    def surfaceContainerHigh(self):
        return argbToQColor(self.scheme.surfaceContainerHigh)

    @property
    def surfaceContainerHighest(self):
        return argbToQColor(self.scheme.surfaceContainerHighest)

    @property
    def surfaceVariant(self):
        return argbToQColor(self.scheme.surfaceVariant)

    @property
    def surfaceBright(self):
        return argbToQColor(self.scheme.surfaceBright)

    @property
    def onSurfaceVariant(self):
        return argbToQColor(self.scheme.onSurfaceVariant)

    @property
    def outline(self):
        return argbToQColor(self.scheme.outline)

    @property
    def outlineVariant(self):
        return argbToQColor(self.scheme.outlineVariant)

    @property
    def shadow(self):
        return argbToQColor(self.scheme.shadow)

    @property
    def inverseSurface(self):
        return argbToQColor(self.scheme.inverseSurface)

    @property
    def inverseOnSurface(self):
        return argbToQColor(self.scheme.inverseOnSurface)

    @property
    def inversePrimary(self):
        return argbToQColor(self.scheme.inversePrimary)

    @property
    def scheme(self) -> Scheme:
        return self.darkScheme if isDarkTheme() else self.lightScheme

    @property
    def reverseScheme(self) -> Scheme:
        return self.lightScheme if isDarkTheme() else self.darkScheme

    @property
    def darkScheme(self) -> Scheme:
        return self.palette['dark']

    @property
    def lightScheme(self) -> Scheme:
        return self.palette['light']

    def colors(self):
        return {n: argbToQColor(argb) for n, argb in self.scheme.props.items()}


class ThemePalette(Palette):

    def __init__(self):
        super().__init__(qconfig.get(qconfig.themeColor))
        qconfig.themeColorChanged.connect(self.setThemeColor)


palette = ThemePalette()


def mixPrimary(color: QColor, weight: float):
    """ mix color with primary color

    Parameters
    ----------
    color: QColor
        the color to be mixed

    weight: float
        the weight of primary color
    """
    return mixColor(themeColor(), color, weight)


def hoverMixPrimary(color: QColor):
    """ mix color with primary color on hover state """
    return mixPrimary(color, 0.08)


def pressedMixPrimary(color: QColor):
    """ mix color with primary color on pressed state """
    return mixPrimary(color, 0.12)