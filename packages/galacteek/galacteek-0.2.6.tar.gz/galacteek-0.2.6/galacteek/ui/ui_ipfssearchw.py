# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/ipfssearchw.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IPFSSearchMain(object):
    def setupUi(self, IPFSSearchMain):
        IPFSSearchMain.setObjectName("IPFSSearchMain")
        IPFSSearchMain.resize(576, 401)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(IPFSSearchMain)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboPages = QtWidgets.QComboBox(IPFSSearchMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboPages.sizePolicy().hasHeightForWidth())
        self.comboPages.setSizePolicy(sizePolicy)
        self.comboPages.setMinimumSize(QtCore.QSize(140, 0))
        self.comboPages.setObjectName("comboPages")
        self.horizontalLayout.addWidget(self.comboPages)
        self.prevPageButton = QtWidgets.QPushButton(IPFSSearchMain)
        self.prevPageButton.setText("")
        self.prevPageButton.setObjectName("prevPageButton")
        self.horizontalLayout.addWidget(self.prevPageButton)
        self.nextPageButton = QtWidgets.QPushButton(IPFSSearchMain)
        self.nextPageButton.setText("")
        self.nextPageButton.setObjectName("nextPageButton")
        self.horizontalLayout.addWidget(self.nextPageButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelInfo = QtWidgets.QLabel(IPFSSearchMain)
        self.labelInfo.setText("")
        self.labelInfo.setObjectName("labelInfo")
        self.horizontalLayout.addWidget(self.labelInfo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(IPFSSearchMain)
        QtCore.QMetaObject.connectSlotsByName(IPFSSearchMain)

    def retranslateUi(self, IPFSSearchMain):
        _translate = QtCore.QCoreApplication.translate
        IPFSSearchMain.setWindowTitle(_translate("IPFSSearchMain", "Form"))

