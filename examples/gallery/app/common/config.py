# coding:utf-8
from enum import Enum

from PySide6.QtCore import QLocale
from qmaterialwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = 2023
AUTHOR = "zhiyiYo"
VERSION = __version__
HELP_URL = "https://qmaterialwidgets.readthedocs.io/zh_CN/latest"
REPO_URL = "https://github.com/zhiyiYo/QMaterialWidgets"
EXAMPLE_URL = "https://github.com/zhiyiYo/QMaterialWidgets/tree/master/examples"
FEEDBACK_URL = "https://github.com/zhiyiYo/QMaterialWidgets/issues"
RELEASE_URL = "https://github.com/zhiyiYo/QMaterialWidgets/releases/latest"
SUPPORT_URL = "https://afdian.net/a/zhiyiYo"


cfg = Config()
qconfig.load('app/config/config.json', cfg)