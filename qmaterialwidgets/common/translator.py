# coding: utf-8
from PyQt5.QtCore import QTranslator, QLocale


class MaterialTranslator(QTranslator):
    """ Translator of fluent widgets """

    def __init__(self, locale: QLocale = None, parent=None):
        super().__init__(parent=parent)
        self.load(locale or QLocale())

    def load(self, locale: QLocale):
        """ load translation file """
        super().load(f":/qmaterialwidgets/i18n/qmaterialwidgets.{locale.name()}.qm")