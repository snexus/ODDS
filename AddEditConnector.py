# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddEditConnector.ui'
#
# Created: Sat Feb 11 12:54:04 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddConnDialog(object):
    def setupUi(self, AddConnDialog):
        AddConnDialog.setObjectName(_fromUtf8("AddConnDialog"))
        AddConnDialog.resize(324, 207)
        self.gridLayout_2 = QtGui.QGridLayout(AddConnDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(AddConnDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.typeBox = QtGui.QComboBox(AddConnDialog)
        self.typeBox.setMaximumSize(QtCore.QSize(16777215, 16777212))
        self.typeBox.setObjectName(_fromUtf8("typeBox"))
        self.typeBox.addItem(_fromUtf8(""))
        self.typeBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.typeBox, 0, 1, 1, 1)
        self.label = QtGui.QLabel(AddConnDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.startNode = QtGui.QComboBox(AddConnDialog)
        self.startNode.setObjectName(_fromUtf8("startNode"))
        self.gridLayout.addWidget(self.startNode, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(AddConnDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.endNode = QtGui.QComboBox(AddConnDialog)
        self.endNode.setObjectName(_fromUtf8("endNode"))
        self.gridLayout.addWidget(self.endNode, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(AddConnDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.editValue = QtGui.QLineEdit(AddConnDialog)
        self.editValue.setObjectName(_fromUtf8("editValue"))
        self.gridLayout.addWidget(self.editValue, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(200, 28, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.line = QtGui.QFrame(AddConnDialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton = QtGui.QPushButton(AddConnDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(AddConnDialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.line_2 = QtGui.QFrame(AddConnDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(AddConnDialog)
        self.label_5.setEnabled(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.modalDamping_edit = QtGui.QLineEdit(AddConnDialog)
        self.modalDamping_edit.setEnabled(False)
        self.modalDamping_edit.setObjectName(_fromUtf8("modalDamping_edit"))
        self.horizontalLayout_2.addWidget(self.modalDamping_edit)
        self.modalDamping_pushbutton = QtGui.QPushButton(AddConnDialog)
        self.modalDamping_pushbutton.setEnabled(False)
        self.modalDamping_pushbutton.setObjectName(_fromUtf8("modalDamping_pushbutton"))
        self.horizontalLayout_2.addWidget(self.modalDamping_pushbutton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 2)

        self.retranslateUi(AddConnDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), AddConnDialog.accept)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), AddConnDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddConnDialog)

    def retranslateUi(self, AddConnDialog):
        AddConnDialog.setWindowTitle(QtGui.QApplication.translate("AddConnDialog", "Add/Edit Connector", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddConnDialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.typeBox.setItemText(0, QtGui.QApplication.translate("AddConnDialog", "Spring", None, QtGui.QApplication.UnicodeUTF8))
        self.typeBox.setItemText(1, QtGui.QApplication.translate("AddConnDialog", "Damping", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddConnDialog", "Start Node:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddConnDialog", "End Node:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AddConnDialog", "Value:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("AddConnDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("AddConnDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AddConnDialog", "Modal Damping Ratio:", None, QtGui.QApplication.UnicodeUTF8))
        self.modalDamping_pushbutton.setText(QtGui.QApplication.translate("AddConnDialog", "Calculate", None, QtGui.QApplication.UnicodeUTF8))
