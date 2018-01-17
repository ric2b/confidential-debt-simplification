# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'invite.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InviteDialog(object):
    def setupUi(self, InviteDialog):
        InviteDialog.setObjectName("InviteDialog")
        InviteDialog.resize(443, 115)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(InviteDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.id_label = QtWidgets.QLabel(InviteDialog)
        self.id_label.setObjectName("id_label")
        self.verticalLayout_2.addWidget(self.id_label)
        self.email_label = QtWidgets.QLabel(InviteDialog)
        self.email_label.setObjectName("email_label")
        self.verticalLayout_2.addWidget(self.email_label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.id_lineedit = QtWidgets.QLineEdit(InviteDialog)
        self.id_lineedit.setPlaceholderText("")
        self.id_lineedit.setObjectName("id_lineedit")
        self.verticalLayout.addWidget(self.id_lineedit)
        self.email_lineedit = QtWidgets.QLineEdit(InviteDialog)
        self.email_lineedit.setMaxLength(160)
        self.email_lineedit.setObjectName("email_lineedit")
        self.verticalLayout.addWidget(self.email_lineedit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.button_box = QtWidgets.QDialogButtonBox(InviteDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_3.addWidget(self.button_box)
        self.id_label.setBuddy(self.id_lineedit)
        self.email_label.setBuddy(self.email_lineedit)

        self.retranslateUi(InviteDialog)
        self.button_box.accepted.connect(InviteDialog.accept)
        self.button_box.rejected.connect(InviteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InviteDialog)

    def retranslateUi(self, InviteDialog):
        _translate = QtCore.QCoreApplication.translate
        InviteDialog.setWindowTitle(_translate("InviteDialog", "Dialog"))
        self.id_label.setText(_translate("InviteDialog", "Invitee ID:"))
        self.email_label.setText(_translate("InviteDialog", "Invitee email:"))
        self.email_lineedit.setPlaceholderText(_translate("InviteDialog", "example@email.com"))

