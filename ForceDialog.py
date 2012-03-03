# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ForceDialog.ui'
#
# Created: Sat Jan  7 14:26:53 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ForceDialog(object):
    def setupUi(self, ForceDialog):
        ForceDialog.setObjectName(_fromUtf8("ForceDialog"))
        ForceDialog.resize(194, 115)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ForceDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(ForceDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxNode = QtGui.QComboBox(ForceDialog)
        self.comboBoxNode.setObjectName(_fromUtf8("comboBoxNode"))
        self.horizontalLayout.addWidget(self.comboBoxNode)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.EditButton = QtGui.QPushButton(ForceDialog)
        self.EditButton.setObjectName(_fromUtf8("EditButton"))
        self.horizontalLayout_2.addWidget(self.EditButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ForceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ForceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ForceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ForceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ForceDialog)

    def retranslateUi(self, ForceDialog):
        ForceDialog.setWindowTitle(QtGui.QApplication.translate("ForceDialog", "Add/Edit Force", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ForceDialog", "Node:", None, QtGui.QApplication.UnicodeUTF8))
        self.EditButton.setText(QtGui.QApplication.translate("ForceDialog", "Edit Function", None, QtGui.QApplication.UnicodeUTF8))

