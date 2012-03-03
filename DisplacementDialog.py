# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DisplacementDialog.ui'
#
# Created: Fri Jan  6 21:14:43 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(207, 260)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBoxNode = QtGui.QComboBox(Dialog)
        self.comboBoxNode.setObjectName(_fromUtf8("comboBoxNode"))
        self.horizontalLayout.addWidget(self.comboBoxNode)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButtonFixed = QtGui.QRadioButton(Dialog)
        self.radioButtonFixed.setChecked(True)
        self.radioButtonFixed.setObjectName(_fromUtf8("radioButtonFixed"))
        self.verticalLayout.addWidget(self.radioButtonFixed)
        self.radioButtonFunction = QtGui.QRadioButton(Dialog)
        self.radioButtonFunction.setObjectName(_fromUtf8("radioButtonFunction"))
        self.verticalLayout.addWidget(self.radioButtonFunction)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setEnabled(False)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBoxType = QtGui.QComboBox(self.groupBox)
        self.comboBoxType.setObjectName(_fromUtf8("comboBoxType"))
        self.comboBoxType.addItem(_fromUtf8(""))
        self.comboBoxType.addItem(_fromUtf8(""))
        self.comboBoxType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxType, 0, 1, 1, 1)
        self.buttonDefine = QtGui.QPushButton(self.groupBox)
        self.buttonDefine.setObjectName(_fromUtf8("buttonDefine"))
        self.gridLayout.addWidget(self.buttonDefine, 1, 0, 1, 2)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        spacerItem = QtGui.QSpacerItem(17, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.radioButtonFunction, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.groupBox.setEnabled)
        QtCore.QObject.connect(self.radioButtonFixed, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.groupBox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Define Displacement", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Node:", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonFixed.setText(QtGui.QApplication.translate("Dialog", "Fixed Condition", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonFunction.setText(QtGui.QApplication.translate("Dialog", "Function", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxType.setItemText(0, QtGui.QApplication.translate("Dialog", "Displacement", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxType.setItemText(1, QtGui.QApplication.translate("Dialog", "Velocity", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxType.setItemText(2, QtGui.QApplication.translate("Dialog", "Acceleration", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDefine.setText(QtGui.QApplication.translate("Dialog", "Define", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))

