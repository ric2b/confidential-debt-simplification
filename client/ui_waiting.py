# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waiting.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WaitingDialog(object):
    def setupUi(self, WaitingDialog):
        WaitingDialog.setObjectName("WaitingDialog")
        WaitingDialog.resize(495, 235)
        self.verticalLayout = QtWidgets.QVBoxLayout(WaitingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(WaitingDialog)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setObjectName("table")
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_all_button = QtWidgets.QPushButton(WaitingDialog)
        self.select_all_button.setObjectName("select_all_button")
        self.horizontalLayout.addWidget(self.select_all_button)
        self.select_none_button = QtWidgets.QPushButton(WaitingDialog)
        self.select_none_button.setObjectName("select_none_button")
        self.horizontalLayout.addWidget(self.select_none_button)
        self.button_box = QtWidgets.QDialogButtonBox(WaitingDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WaitingDialog)
        self.button_box.accepted.connect(WaitingDialog.accept)
        self.button_box.rejected.connect(WaitingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WaitingDialog)

    def retranslateUi(self, WaitingDialog):
        _translate = QtCore.QCoreApplication.translate
        WaitingDialog.setWindowTitle(_translate("WaitingDialog", "Dialog"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("WaitingDialog", "ID"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("WaitingDialog", "Loaner"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("WaitingDialog", "Amount"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("WaitingDialog", "Description"))
        self.select_all_button.setText(_translate("WaitingDialog", "Select All"))
        self.select_none_button.setText(_translate("WaitingDialog", "Select None"))

