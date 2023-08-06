# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/henriquegemignani/randovania/randovania/gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 560)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.progress_box = QtWidgets.QGroupBox(self.centralWidget)
        self.progress_box.setObjectName("progress_box")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.progress_box)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.progress_bar = QtWidgets.QProgressBar(self.progress_box)
        self.progress_bar.setMinimumSize(QtCore.QSize(200, 0))
        self.progress_bar.setMaximumSize(QtCore.QSize(250, 16777215))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout_3.addWidget(self.progress_bar, 0, 0, 1, 2)
        self.progress_label = QtWidgets.QLabel(self.progress_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy)
        self.progress_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.progress_label.setText("")
        self.progress_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progress_label.setObjectName("progress_label")
        self.gridLayout_3.addWidget(self.progress_label, 0, 2, 1, 1)
        self.stop_background_process_button = QtWidgets.QPushButton(self.progress_box)
        self.stop_background_process_button.setEnabled(False)
        self.stop_background_process_button.setMinimumSize(QtCore.QSize(100, 0))
        self.stop_background_process_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.stop_background_process_button.setCheckable(False)
        self.stop_background_process_button.setFlat(False)
        self.stop_background_process_button.setObjectName("stop_background_process_button")
        self.gridLayout_3.addWidget(self.stop_background_process_button, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.progress_box)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Randovania"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Randovania</span></p><p><a href=\"https://github.com/henriquegemignani/randovania\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://github.com/henriquegemignani/randovania</span></a></p><p><span style=\" font-size:10pt;\">This software is covered by the </span><a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">GNU General Public License v3 (GPL v3)</span></a><span style=\" font-size:10pt;\">.</span></p><p><br/></p><p><span style=\" font-size:12pt;\">Community</span></p><p><span style=\" font-size:10pt;\">Make sure to visit the Metroid Prime Randomizer Discord server!</span><br/><a href=\"https://discordapp.com/invite/gymstUz\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://discordapp.com/invite/gymstUz</span></a></p><p><br/></p><p><span style=\" font-size:12pt;\">Credits</span><br/><br/><span style=\" font-size:10pt;\">Written by </span><a href=\"https://github.com/henriquegemignani/\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Henrique Gemignani</span></a></p><p><span style=\" font-size:10pt;\">Metroid Prime 2 room data collected by </span><a href=\"https://twitter.com/ClarisRobyn\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Claris</span></a></p><p><span style=\" font-size:10pt;\">Randomizer also written by Claris</span></p><p><span style=\" font-size:10pt;\">BashPrime, Pwootage, and April Wade made </span><a href=\"https://randomizer.metroidprime.run/\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://randomizer.metroidprime.run/</span></a><span style=\" font-size:10pt;\">, from which the GUI was based.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "About"))
        self.progress_box.setTitle(_translate("MainWindow", "Progress"))
        self.stop_background_process_button.setText(_translate("MainWindow", "Stop"))

