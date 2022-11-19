# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerTnTKrW.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)

from PyQt5.QtWidgets import *
from MyPyQtClass import MyTableWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.NonModal)
        Form.setEnabled(True)
        Form.resize(344, 266)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 341, 261))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget = QWidget(self.tab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(1, 10, 331, 221))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cb_old = QCheckBox(self.verticalLayoutWidget)
        self.cb_old.setObjectName(u"cb_old")

        self.horizontalLayout_2.addWidget(self.cb_old)

        self.cb_cbss = QCheckBox(self.verticalLayoutWidget)
        self.cb_cbss.setObjectName(u"cb_cbss")

        self.horizontalLayout_2.addWidget(self.cb_cbss)

        self.cb_dd = QCheckBox(self.verticalLayoutWidget)
        self.cb_dd.setObjectName(u"cb_dd")

        self.horizontalLayout_2.addWidget(self.cb_dd)

        self.cb_second = QCheckBox(self.verticalLayoutWidget)
        self.cb_second.setObjectName(u"cb_second")

        self.horizontalLayout_2.addWidget(self.cb_second)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_login = QPushButton(self.verticalLayoutWidget)
        self.btn_login.setObjectName(u"btn_login")

        self.horizontalLayout_3.addWidget(self.btn_login)

        self.btn_watch = QPushButton(self.verticalLayoutWidget)
        self.btn_watch.setObjectName(u"btn_watch")

        self.horizontalLayout_3.addWidget(self.btn_watch)

        self.btn_open = QPushButton(self.verticalLayoutWidget)
        self.btn_open.setObjectName(u"btn_open")

        self.horizontalLayout_3.addWidget(self.btn_open)

        self.btn_close = QPushButton(self.verticalLayoutWidget)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.te_output = QTextEdit(self.verticalLayoutWidget)
        self.te_output.setObjectName(u"te_output")

        self.horizontalLayout_4.addWidget(self.te_output)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayoutWidget = QWidget(self.tab_2)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 331, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.horizontalLayoutWidget_2 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 30, 331, 201))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tw_dd_output = MyTableWidget(self.horizontalLayoutWidget_2)
        self.tw_dd_output.setObjectName(u"tw_dd_output")
        self.tw_dd_output.setRowCount(0)
        self.tw_dd_output.setColumnCount(0)

        self.horizontalLayout_5.addWidget(self.tw_dd_output)

        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"KB", None))
        self.cb_old.setText(QCoreApplication.translate("Form", u"old", None))
        self.cb_cbss.setText(QCoreApplication.translate("Form", u"cbss", None))
        self.cb_dd.setText(QCoreApplication.translate("Form", u"dd", None))
        self.cb_second.setText(QCoreApplication.translate("Form", u"2", None))
        self.btn_login.setText(QCoreApplication.translate("Form", u"&Login", None))
        self.btn_watch.setText(QCoreApplication.translate("Form", u"&Watch", None))
        self.btn_open.setText(QCoreApplication.translate("Form", u"&Open", None))
        self.btn_close.setText(QCoreApplication.translate("Form", u"&Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
    # retranslateUi

