#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets


def cryostream():
    from .gui.wcryo import WCryo
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    wcryo = WCryo(None)
    wcryo.loadSettings()
    wcryo.show()
    ret = app.exec()
    wcryo.saveSettings()
    sys.exit(ret)


def blower():
    from .gui.wblower import WBlower
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    wblower = WBlower(None)
    wblower.loadSettings()
    wblower.show()
    ret = app.exec()
    wblower.saveSettings()
    sys.exit(ret)


def wscripted():
    from .gui.wscripted import WScriptEd
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    ww = WScriptEd(None, {})
    ww.loadSettings()
    ww.show()
    ret = app.exec()
    ww.saveSettings()
    sys.exit(ret)


def wseq():
    from .gui.wseq import WSeq
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    ww = WSeq(None)
    ww.loadSettings()
    ww.show()
    ret = app.exec()
    ww.saveSettings()
    sys.exit(ret)


def lakeshore():
    from .gui.wlakeshore import WLakeshore
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    wwlakeshore = WLakeshore(None)
    wwlakeshore.loadSettings()
    wwlakeshore.show()
    ret = app.exec()
    wwlakeshore.saveSettings()
    sys.exit(ret)


def iseg():
    from .gui.wiseg import WIseg
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    wiseg = WIseg(None)
    wiseg.loadSettings()
    wiseg.show()
    ret = app.exec()
    wiseg.saveSettings()
    sys.exit(ret)
