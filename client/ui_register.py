# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        RegisterDialog.setObjectName("RegisterDialog")
        RegisterDialog.resize(460, 299)
        self.verticalLayout = QtWidgets.QVBoxLayout(RegisterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.id_label = QtWidgets.QLabel(RegisterDialog)
        self.id_label.setObjectName("id_label")
        self.horizontalLayout_3.addWidget(self.id_label)
        self.id_line = QtWidgets.QLineEdit(RegisterDialog)
        self.id_line.setReadOnly(True)
        self.id_line.setObjectName("id_line")
        self.horizontalLayout_3.addWidget(self.id_line)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.inviter_label = QtWidgets.QLabel(RegisterDialog)
        self.inviter_label.setObjectName("inviter_label")
        self.horizontalLayout_7.addWidget(self.inviter_label)
        self.inviter_line = QtWidgets.QLineEdit(RegisterDialog)
        self.inviter_line.setObjectName("inviter_line")
        self.horizontalLayout_7.addWidget(self.inviter_line)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.email_label = QtWidgets.QLabel(RegisterDialog)
        self.email_label.setObjectName("email_label")
        self.horizontalLayout_5.addWidget(self.email_label)
        self.email_line = QtWidgets.QLineEdit(RegisterDialog)
        self.email_line.setObjectName("email_line")
        self.horizontalLayout_5.addWidget(self.email_line)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.group_label = QtWidgets.QLabel(RegisterDialog)
        self.group_label.setObjectName("group_label")
        self.horizontalLayout_4.addWidget(self.group_label)
        self.group_line = QtWidgets.QLineEdit(RegisterDialog)
        self.group_line.setObjectName("group_line")
        self.horizontalLayout_4.addWidget(self.group_line)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.group_key_label = QtWidgets.QLabel(RegisterDialog)
        self.group_key_label.setObjectName("group_key_label")
        self.horizontalLayout_6.addWidget(self.group_key_label)
        self.group_key_line = QtWidgets.QLineEdit(RegisterDialog)
        self.group_key_line.setObjectName("group_key_line")
        self.horizontalLayout_6.addWidget(self.group_key_line)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.secret_label = QtWidgets.QLabel(RegisterDialog)
        self.secret_label.setObjectName("secret_label")
        self.horizontalLayout.addWidget(self.secret_label)
        self.secret_line = QtWidgets.QLineEdit(RegisterDialog)
        self.secret_line.setObjectName("secret_line")
        self.horizontalLayout.addWidget(self.secret_line)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.password_label = QtWidgets.QLabel(RegisterDialog)
        self.password_label.setObjectName("password_label")
        self.horizontalLayout_2.addWidget(self.password_label)
        self.password_line = QtWidgets.QLineEdit(RegisterDialog)
        self.password_line.setMaxLength(256)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setObjectName("password_line")
        self.horizontalLayout_2.addWidget(self.password_line)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(RegisterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.id_label.setBuddy(self.id_line)
        self.inviter_label.setBuddy(self.secret_line)
        self.email_label.setBuddy(self.secret_line)
        self.group_label.setBuddy(self.secret_line)
        self.group_key_label.setBuddy(self.secret_line)
        self.secret_label.setBuddy(self.secret_line)
        self.password_label.setBuddy(self.password_line)

        self.retranslateUi(RegisterDialog)
        self.buttonBox.accepted.connect(RegisterDialog.accept)
        self.buttonBox.rejected.connect(RegisterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegisterDialog)

    def retranslateUi(self, RegisterDialog):
        _translate = QtCore.QCoreApplication.translate
        RegisterDialog.setWindowTitle(_translate("RegisterDialog", "Dialog"))
        self.id_label.setText(_translate("RegisterDialog", "Your ID:"))
        self.inviter_label.setText(_translate("RegisterDialog", "Inviter ID:"))
        self.inviter_line.setPlaceholderText(_translate("RegisterDialog", "paste ID of the inviter"))
        self.email_label.setText(_translate("RegisterDialog", "Email:"))
        self.email_line.setPlaceholderText(_translate("RegisterDialog", "example@email.com"))
        self.group_label.setText(_translate("RegisterDialog", "Group:"))
        self.group_line.setPlaceholderText(_translate("RegisterDialog", "group server URL..."))
        self.group_key_label.setText(_translate("RegisterDialog", "Group Key:"))
        self.group_key_line.setPlaceholderText(_translate("RegisterDialog", "group server public key..."))
        self.secret_label.setText(_translate("RegisterDialog", "Secret:"))
        self.secret_line.setPlaceholderText(_translate("RegisterDialog", "paste secret code..."))
        self.password_label.setText(_translate("RegisterDialog", "Password:"))
        self.password_line.setPlaceholderText(_translate("RegisterDialog", "type secure password..."))

