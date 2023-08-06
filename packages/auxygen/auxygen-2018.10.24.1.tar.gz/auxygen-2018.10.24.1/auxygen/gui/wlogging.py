#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from qtsnbl.widgets import FixedWidget
from .ui.ui_wlogging import Ui_WLogging


class WLogging(QtWidgets.QDialog, Ui_WLogging, FixedWidget):
    sigClosed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        self.hide()
        self.saveSettings()
        self.sigClosed.emit()
        super().closeEvent(event)

    def saveSettings(self):
        s = QtCore.QSettings()
        s.setValue('WLogging/Geometry', self.saveGeometry())

    def loadSettings(self):
        s = QtCore.QSettings()
        self.restoreGeometry(s.value('WLogging/Geometry', b''))

    def postLogMessage(self, message):
        self.loggingTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.loggingTextEdit.insertPlainText(message)
