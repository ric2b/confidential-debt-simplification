# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uome.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UOMeDialog(object):
    def setupUi(self, UOMeDialog):
        UOMeDialog.setObjectName("UOMeDialog")
        UOMeDialog.resize(443, 150)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(UOMeDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.borrower_label = QtWidgets.QLabel(UOMeDialog)
        self.borrower_label.setObjectName("borrower_label")
        self.verticalLayout_2.addWidget(self.borrower_label)
        self.amount_label = QtWidgets.QLabel(UOMeDialog)
        self.amount_label.setObjectName("amount_label")
        self.verticalLayout_2.addWidget(self.amount_label)
        self.description_label = QtWidgets.QLabel(UOMeDialog)
        self.description_label.setObjectName("description_label")
        self.verticalLayout_2.addWidget(self.description_label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.borrower_lineedit = QtWidgets.QLineEdit(UOMeDialog)
        self.borrower_lineedit.setObjectName("borrower_lineedit")
        self.verticalLayout.addWidget(self.borrower_lineedit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.amount_spinbox = QtWidgets.QDoubleSpinBox(UOMeDialog)
        self.amount_spinbox.setMaximum(999999.99)
        self.amount_spinbox.setProperty("value", 1.0)
        self.amount_spinbox.setObjectName("amount_spinbox")
        self.horizontalLayout_2.addWidget(self.amount_spinbox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.description_lineedit = QtWidgets.QLineEdit(UOMeDialog)
        self.description_lineedit.setMaxLength(160)
        self.description_lineedit.setObjectName("description_lineedit")
        self.verticalLayout.addWidget(self.description_lineedit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.button_box = QtWidgets.QDialogButtonBox(UOMeDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_3.addWidget(self.button_box)
        self.borrower_label.setBuddy(self.borrower_lineedit)
        self.amount_label.setBuddy(self.amount_spinbox)
        self.description_label.setBuddy(self.description_lineedit)

        self.retranslateUi(UOMeDialog)
        self.button_box.accepted.connect(UOMeDialog.accept)
        self.button_box.rejected.connect(UOMeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UOMeDialog)

    def retranslateUi(self, UOMeDialog):
        _translate = QtCore.QCoreApplication.translate
        UOMeDialog.setWindowTitle(_translate("UOMeDialog", "Dialog"))
        self.borrower_label.setText(_translate("UOMeDialog", "Borrower:"))
        self.amount_label.setText(_translate("UOMeDialog", "Amount:"))
        self.description_label.setText(_translate("UOMeDialog", "Description:"))
        self.borrower_lineedit.setPlaceholderText(_translate("UOMeDialog", "borrower ID or email"))
        self.description_lineedit.setPlaceholderText(_translate("UOMeDialog", "short description..."))

