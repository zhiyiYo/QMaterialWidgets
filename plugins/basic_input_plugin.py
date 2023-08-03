# coding: utf-8
from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from qmaterialwidgets import (FilledPushButton, FluentIcon, SwitchButton, RadioButton, CheckBox, Slider,
                              ComboBox, IconWidget, OutlinedPushButton, FilledToolButton,
                              TransparentToolButton, TransparentToggleToolButton, OutlinedToggleToolButton,
                              OutlinedToolButton, TextPushButton, TonalPushButton, TonalToolButton,
                              ElevatedPushButton, FilledToggleToolButton, FilledComboBox, SurfaceFloatingActionButton,
                              PrimaryFloatingActionButton, TertiaryFloatingActionButton, SecondaryFloatingActionButton,
                              InputChip, FilterChip, ElevatedInputChip, ElevatedFilterChip, FilledDropDownPushButton,
                              TextDropDownPushButton, TonalDropDownPushButton, ElevatedDropDownPushButton,
                              OutlinedDropDownPushButton)

from plugin_base import PluginBase
from task_menu_factory import EditTextTaskMenuFactory


class BasicInputPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Basic Input)'


class TextPlugin(BasicInputPlugin):

    def domXml(self):
        return f"""
        <widget class="{self.name()}" name="{self.name()}">
            <property name="text">
                <string>{self.toolTip()}</string>
            </property>
        </widget>
        """


class CheckBoxPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Check box plugin """

    def createWidget(self, parent):
        return CheckBox(self.toolTip(), parent)

    def icon(self):
        return super().icon('Checkbox')

    def name(self):
        return "CheckBox"


class ComboBoxPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Combo box plugin """

    def createWidget(self, parent):
        return ComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "ComboBox"


class FilledComboBoxPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Filled combo box plugin """

    def createWidget(self, parent):
        return FilledComboBox(parent)

    def icon(self):
        return super().icon('ComboBox')

    def name(self):
        return "FilledComboBox"


class OutlinedPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Push button plugin """

    def createWidget(self, parent):
        return OutlinedPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "OutlinedPushButton"


class TextPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Text push button plugin """

    def createWidget(self, parent):
        return TextPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TextPushButton"


class TonalPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Text push button plugin """

    def createWidget(self, parent):
        return TonalPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TonalPushButton"


class ElevatedPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Text push button plugin """

    def createWidget(self, parent):
        return ElevatedPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "ElevatedPushButton"


class FilledPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Filled push button plugin """

    def createWidget(self, parent):
        return FilledPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "FilledPushButton"


class FilledDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Filled drop down push button plugin """

    def createWidget(self, parent):
        return FilledDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "FilledDropDownPushButton"


class ElevatedDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Elevated drop down push button plugin """

    def createWidget(self, parent):
        return ElevatedDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "ElevatedDropDownPushButton"


class OutlinedDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Outlined drop down push button plugin """

    def createWidget(self, parent):
        return OutlinedDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "OutlinedDropDownPushButton"


class TonalDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Tonal drop down push button plugin """

    def createWidget(self, parent):
        return TonalDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "TonalDropDownPushButton"


class TextDropDownPushButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Text drop down push button plugin """

    def createWidget(self, parent):
        return TextDropDownPushButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "TextDropDownPushButton"


class FilledToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Filled tool button plugin """

    def createWidget(self, parent):
        return FilledToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "FilledToolButton"


class OutlinedToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Outlined tool button plugin """

    def createWidget(self, parent):
        return OutlinedToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "OutlinedToolButton"


class TonalToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Tonal tool button plugin """

    def createWidget(self, parent):
        return TonalToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TonalToolButton"


class TransparentToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Transparent tool button plugin """

    def createWidget(self, parent):
        return TransparentToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TransparentToolButton"


class SecondaryFloatingActionButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Secondary floating action button plugin """

    def createWidget(self, parent):
        return SecondaryFloatingActionButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "SecondaryFloatingActionButton"


class TertiaryFloatingActionButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Tertiary floating action button plugin """

    def createWidget(self, parent):
        return TertiaryFloatingActionButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "TertiaryFloatingActionButton"


class PrimaryFloatingActionButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Primary floating action button plugin """

    def createWidget(self, parent):
        return PrimaryFloatingActionButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "PrimaryFloatingActionButton"


class SurfaceFloatingActionButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Surface floating action button plugin """

    def createWidget(self, parent):
        return SurfaceFloatingActionButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "SurfaceFloatingActionButton"


@EditTextTaskMenuFactory.register
class SwitchButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Switch button plugin """

    def createWidget(self, parent):
        return SwitchButton(parent)

    def icon(self):
        return super().icon('ToggleSwitch')

    def name(self):
        return "SwitchButton"


class RadioButtonPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Radio button plugin """

    def createWidget(self, parent):
        return RadioButton(self.toolTip(), parent)

    def icon(self):
        return super().icon('RadioButton')

    def name(self):
        return "RadioButton"


class OutlinedToggleToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Transparent toggle tool button plugin """

    def createWidget(self, parent):
        return OutlinedToggleToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "OutlinedToggleToolButton"


class FilledToggleToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Filled toggle tool button plugin """

    def createWidget(self, parent):
        return FilledToggleToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "FilledToggleToolButton"


class TransparentToggleToolButtonPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Transparent toggle tool button plugin """

    def createWidget(self, parent):
        return TransparentToggleToolButton(FluentIcon.BASKETBALL, parent)

    def icon(self):
        return super().icon('ToggleButton')

    def name(self):
        return "TransparentToggleToolButton"


class SliderPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """  Slider  plugin """

    def createWidget(self, parent):
        slider = Slider(parent)
        slider.setRange(0, 100)
        slider.setMinimumWidth(200)
        return slider

    def icon(self):
        return super().icon('Slider')

    def name(self):
        return "Slider"


class IconWidgetPlugin(BasicInputPlugin, QDesignerCustomWidgetInterface):
    """ Icon widget plugin """

    def createWidget(self, parent):
        return IconWidget(FluentIcon.EMOJI_TAB_SYMBOLS, parent)

    def icon(self):
        return super().icon('IconElement')

    def name(self):
        return "IconWidget"


class InputChipPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Input chip plugin """

    def createWidget(self, parent):
        return InputChip(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "InputChip"


class ElevatedInputChipPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Elevated input chip plugin """

    def createWidget(self, parent):
        return ElevatedInputChip(self.toolTip(), parent)

    def icon(self):
        return super().icon('Button')

    def name(self):
        return "ElevatedInputChip"


class FilterChipPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Input chip plugin """

    def createWidget(self, parent):
        return FilterChip(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "FilterChip"


class ElevatedFilterChipPlugin(TextPlugin, QDesignerCustomWidgetInterface):
    """ Elevated filter chip plugin """

    def createWidget(self, parent):
        return ElevatedFilterChip(self.toolTip(), parent)

    def icon(self):
        return super().icon('DropDownButton')

    def name(self):
        return "ElevatedFilterChip"
