#!/usr/bin/env python

"""
mplcurveplugin.py

Matplotlib curve plotting widget plugin for Qt Designer.

Copyright (C) 2018 Tong Zhang <zhangt@frib.msu.edu>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from mpl4qt.widgets.mplcurvewidget import MatplotlibCurveWidget
from mpl4qt.icons import mplcurvewidget_icon


class MatplotlibCurveWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    """MatplotlibCurveWidgetPlugin(QPyDesignerCustomWidgetPlugin)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """
    def __init__(self, parent=None):
        super(MatplotlibCurveWidgetPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return MatplotlibCurveWidget(parent)

    def name(self):
        return "MatplotlibCurveWidget"

    def group(self):
        return "DataViz Widgets"

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="MatplotlibCurveWidget" name="matplotlibcurveWidget" />\n'

    def includeFile(self):
        return "mpl4qt.widgets.mplcurvewidget"

# Define the image used for the icon.
_logo_pixmap = QPixmap(mplcurvewidget_icon)
