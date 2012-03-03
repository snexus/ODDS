# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MassDlg.ui'
#
# Created: Fri Jan  6 21:14:41 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MassDialog(object):
    def setupUi(self, MassDialog):
        MassDialog.setObjectName(_fromUtf8("MassDialog"))
        MassDialog.resize(219, 117)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        MassDialog.setFont(font)
        self.horizontalLayout = QtGui.QHBoxLayout(MassDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(MassDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mass_node = QtGui.QComboBox(MassDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.mass_node.setFont(font)
        self.mass_node.setObjectName(_fromUtf8("mass_node"))
        self.gridLayout.addWidget(self.mass_node, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(MassDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.mass_value = QtGui.QLineEdit(MassDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.mass_value.setFont(font)
        self.mass_value.setObjectName(_fromUtf8("mass_value"))
        self.gridLayout.addWidget(self.mass_value, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(MassDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MassDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MassDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MassDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MassDialog)

    def retranslateUi(self, MassDialog):
        MassDialog.setWindowTitle(QtGui.QApplication.translate("MassDialog", "Add/Edit Mass", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MassDialog", "Node:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MassDialog", "Value", None, QtGui.QApplication.UnicodeUTF8))

