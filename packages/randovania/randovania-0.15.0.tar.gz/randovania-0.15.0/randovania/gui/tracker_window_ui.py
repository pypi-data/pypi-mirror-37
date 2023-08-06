# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/henriquegemignani/randovania/randovania/gui/tracker_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TrackerWindow(object):
    def setupUi(self, TrackerWindow):
        TrackerWindow.setObjectName("TrackerWindow")
        TrackerWindow.resize(802, 488)
        self.centralWidget = QtWidgets.QWidget(TrackerWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.items_tree_widget = QtWidgets.QTreeWidget(self.groupBox)
        self.items_tree_widget.setGeometry(QtCore.QRect(30, 70, 671, 91))
        self.items_tree_widget.setObjectName("items_tree_widget")
        self.events_list_widget = QtWidgets.QListWidget(self.groupBox)
        self.events_list_widget.setGeometry(QtCore.QRect(40, 240, 611, 91))
        self.events_list_widget.setObjectName("events_list_widget")
        self._events_list_header = QtWidgets.QLabel(self.groupBox)
        self._events_list_header.setGeometry(QtCore.QRect(50, 200, 47, 13))
        self._events_list_header.setObjectName("_events_list_header")
        self.current_location_label = QtWidgets.QLabel(self.groupBox)
        self.current_location_label.setGeometry(QtCore.QRect(30, 40, 331, 16))
        self.current_location_label.setObjectName("current_location_label")
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        TrackerWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(TrackerWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menuBar.setObjectName("menuBar")
        TrackerWindow.setMenuBar(self.menuBar)

        self.retranslateUi(TrackerWindow)
        QtCore.QMetaObject.connectSlotsByName(TrackerWindow)

    def retranslateUi(self, TrackerWindow):
        _translate = QtCore.QCoreApplication.translate
        TrackerWindow.setWindowTitle(_translate("TrackerWindow", "Tracker"))
        self.groupBox.setTitle(_translate("TrackerWindow", "GroupBox"))
        self.items_tree_widget.headerItem().setText(0, _translate("TrackerWindow", "Item"))
        self.items_tree_widget.headerItem().setText(1, _translate("TrackerWindow", "Quantity"))
        self.events_list_widget.setSortingEnabled(True)
        self._events_list_header.setText(_translate("TrackerWindow", "Events"))
        self.current_location_label.setText(_translate("TrackerWindow", "Current location:"))

