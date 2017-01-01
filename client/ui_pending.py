# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pending.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PendingDialog(object):
    def setupUi(self, PendingDialog):
        PendingDialog.setObjectName("PendingDialog")
        PendingDialog.resize(495, 235)
        self.verticalLayout = QtWidgets.QVBoxLayout(PendingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(PendingDialog)
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
        self.select_all_button = QtWidgets.QPushButton(PendingDialog)
        self.select_all_button.setObjectName("select_all_button")
        self.horizontalLayout.addWidget(self.select_all_button)
        self.select_none_button = QtWidgets.QPushButton(PendingDialog)
        self.select_none_button.setObjectName("select_none_button")
        self.horizontalLayout.addWidget(self.select_none_button)
        self.button_box = QtWidgets.QDialogButtonBox(PendingDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PendingDialog)
        self.button_box.accepted.connect(PendingDialog.accept)
        self.button_box.rejected.connect(PendingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PendingDialog)

    def retranslateUi(self, PendingDialog):
        _translate = QtCore.QCoreApplication.translate
        PendingDialog.setWindowTitle(_translate("PendingDialog", "Dialog"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("PendingDialog", "Borrower"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("PendingDialog", "Amount"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("PendingDialog", "Description"))
        self.select_all_button.setText(_translate("PendingDialog", "Select All"))
        self.select_none_button.setText(_translate("PendingDialog", "Select None"))

