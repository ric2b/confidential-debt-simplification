# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(401, 80)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.password_label = QtWidgets.QLabel(LoginDialog)
        self.password_label.setObjectName("password_label")
        self.horizontalLayout_3.addWidget(self.password_label)
        self.password_line = QtWidgets.QLineEdit(LoginDialog)
        self.password_line.setText("")
        self.password_line.setMaxLength(256)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setReadOnly(False)
        self.password_line.setObjectName("password_line")
        self.horizontalLayout_3.addWidget(self.password_line)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoginDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.password_label.setBuddy(self.password_line)

        self.retranslateUi(LoginDialog)
        self.buttonBox.accepted.connect(LoginDialog.accept)
        self.buttonBox.rejected.connect(LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Dialog"))
        self.password_label.setText(_translate("LoginDialog", "Password:"))
        self.password_line.setPlaceholderText(_translate("LoginDialog", "type password here..."))

