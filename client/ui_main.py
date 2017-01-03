# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 296)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.info_group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.info_group_box.setObjectName("info_group_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.info_group_box)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.balance_label = QtWidgets.QLabel(self.info_group_box)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.balance_label.setFont(font)
        self.balance_label.setObjectName("balance_label")
        self.horizontalLayout.addWidget(self.balance_label)
        self.balance_value = QtWidgets.QLabel(self.info_group_box)
        self.balance_value.setObjectName("balance_value")
        self.horizontalLayout.addWidget(self.balance_value)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.info_group_box)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.transactions_list = QtWidgets.QListWidget(self.info_group_box)
        self.transactions_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.transactions_list.setObjectName("transactions_list")
        self.verticalLayout_2.addWidget(self.transactions_list)
        self.transactions_list.raise_()
        self.label.raise_()
        self.verticalLayout_3.addWidget(self.info_group_box)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uome_button = QtWidgets.QPushButton(self.centralwidget)
        self.uome_button.setObjectName("uome_button")
        self.horizontalLayout_2.addWidget(self.uome_button)
        self.invite_button = QtWidgets.QPushButton(self.centralwidget)
        self.invite_button.setObjectName("invite_button")
        self.horizontalLayout_2.addWidget(self.invite_button)
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")
        self.horizontalLayout_2.addWidget(self.refresh_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pending_button = QtWidgets.QPushButton(self.centralwidget)
        self.pending_button.setObjectName("pending_button")
        self.horizontalLayout_4.addWidget(self.pending_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.info_group_box.setTitle(_translate("MainWindow", "User: c1@email.com"))
        self.balance_label.setText(_translate("MainWindow", "Balance:"))
        self.balance_value.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "Transactions:"))
        self.transactions_list.setSortingEnabled(True)
        self.uome_button.setText(_translate("MainWindow", "UOMe"))
        self.invite_button.setText(_translate("MainWindow", "Invite"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.pending_button.setText(_translate("MainWindow", "Pending"))

