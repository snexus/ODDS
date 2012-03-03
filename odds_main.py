'''
Created on Dec 30, 2011

@author: Denis
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import AddEditConnector
import MassDlg
import oddsForm
import FunctionDialog
import DisplacementDialog
from math import *


class MainDlg(QDialog,oddsForm.Ui_mainDialog):
    def __init__(self,parent=None):
        super(MainDlg,self).__init__(parent)
        self.setupUi(self)
        self.syst=DynSystem()
        self.nodes_spinBox.setValue(self.syst.n_nodes)
        self.nodes_spinBox.setMinimum(2)
 
        #initialize tables
        self.ConnTableRowCount,self.MassTableRowCount,self.DispTableRowCount=0,0,0
        self.initTables([self.ConnTable,self.MassTable,self.DispTable])

      
        #self.updadeUi()
    
    
    def initTables(self,tables):
        for table in tables:
            table.setAlternatingRowColors(True)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setSelectionMode(QTableWidget.SingleSelection)
    
    @pyqtSignature("")
    def on_DispAddButton_clicked(self):
        available_nodes=self.syst.get_available_mass_nodes()
        if len(available_nodes)==0:
            QMessageBox.warning(self, "Error","No more available nodes for displacements")
            return
        Disp=Displacement(available_nodes)
        if Disp.configure(available_nodes):
            self.syst.addDisplacement(available_nodes[Disp.node], Disp)
            self.DispTableRowCount=self.DispTableRowCount+1
            self.DispTable.setRowCount(self.DispTableRowCount)
            self.setDispTableData(self.DispTableRowCount-1, Disp,available_nodes[Disp.node])
    
    @pyqtSignature("")
    def on_DispEditButton_clicked(self):
        if self.DispTable.hasFocus():
            if self.DispTableRowCount==0:
                return
            row=self.DispTable.currentRow()
            node=self.DispTable.item(row,0).text().toInt()[0]
            available_nodes=self.syst.get_available_mass_nodes()
            available_nodes.append(node-1)
            available_nodes.sort()
            Displacement=self.syst.displacements[node-1]
            if Displacement.configure(available_nodes,available_nodes.index(node-1)+1):
                self.syst.addDisplacement(node-1, delete_flag=1)
                self.syst.addDisplacement(available_nodes[Displacement.node], Displacement)
                self.setDispTableData(row, Displacement,available_nodes[Displacement.node])
    
    @pyqtSignature("")
    def on_DispDelButton_clicked(self):
        if self.DispTable.hasFocus():
            if self.DispTableRowCount==0:
                return
            row=self.DispTable.currentRow()
            node=self.DispTable.item(row,0).text().toInt()[0]
            self.syst.addDisplacement(node-1,delete_flag=1)
            self.DispTableRowCount=self.DispTableRowCount-1
            self.DispTable.removeRow(row)
        else:
            QMessageBox.information(self, "Note","Please select item at mass or displacement table")
        
    def setDispTableData(self,row,Disp,node):
        func={1:'0',2:Disp.custFunc.supported[Disp.custFunc.type]}[Disp.funcType]
        type1={1:'Displacement',2:Disp.supportedMovement[Disp.movementType]}[Disp.funcType]
        value={1:'0',2:Disp.custFunc.getString()}[Disp.funcType]
        self.DispTable.setItem(row,0,QTableWidgetItem(str(node+1)))
        self.DispTable.setItem(row,1,QTableWidgetItem(type1))
        self.DispTable.setItem(row,2,QTableWidgetItem(func))
        self.DispTable.setItem(row,3,QTableWidgetItem(value))
        self.DispTable.resizeColumnsToContents()
        self.DispTable.resizeRowsToContents()
    
    @pyqtSignature("")
    def on_MassAddButton_clicked(self):
        available_mass_nodes=self.syst.get_available_mass_nodes()
        if len(available_mass_nodes)==0:
            QMessageBox.warning(self, "Error","No more available nodes for masses")
            return
        MassDlg=MassDialog(available_mass_nodes)
        if MassDlg.exec_():
            index1,value1=MassDlg.retrieve_data()
            node=available_mass_nodes[index1]
            self.syst.addMass(node,value1)
            self.MassTableRowCount=self.MassTableRowCount+1
            self.MassTable.setRowCount(self.MassTableRowCount)
            self.setMassTableData(self.MassTableRowCount-1, value1, node)
#            self.MassTable.setItem(self.MassTableRowCount-1,0,QTableWidgetItem(str(node+1)))
#            self.MassTable.setItem(self.MassTableRowCount-1,1,QTableWidgetItem(str(value1)))
    
    @pyqtSignature("")
    def on_MassDeleteButton_clicked(self):
        if self.MassTable.hasFocus():
            if self.MassTableRowCount==0:
                return
            row=self.MassTable.currentRow()
            node,value1=self.getMassTableData(row)
            self.syst.addMass(node-1,delete_flag=1)
            self.MassTableRowCount=self.MassTableRowCount-1
            self.MassTable.removeRow(row)
        else:
            QMessageBox.information(self, "Note","Please select item at mass or displacement table")
    
    @pyqtSignature("")
    def on_MassEditButton_clicked(self):
        if self.MassTable.hasFocus():
            if self.MassTableRowCount==0:
                return
            row=self.MassTable.currentRow()
            node,value1=self.getMassTableData(row)
            available_mass_nodes=self.syst.get_available_mass_nodes()
            available_mass_nodes.append(node-1)
            available_mass_nodes.sort()
            node_no=available_mass_nodes.index(node-1)
            
            MassDlg=MassDialog(available_mass_nodes,value1=value1,current_node=node_no)
            if MassDlg.exec_():
                index1,value1=MassDlg.retrieve_data()
                self.syst.addMass(node-1,delete_flag=1)
                node=available_mass_nodes[index1]
                self.syst.addMass(node,value1)
                self.setMassTableData(row,value1,node)
                
    
    @pyqtSignature("")
    def on_ConnAddButton_clicked(self):
        AddEditConnDlg=AddEditConnDialog(0,0,self.syst.n_nodes)
        if AddEditConnDlg.exec_():
            type1,start,end,value=AddEditConnDlg.retrieve_data()
            self.syst.addConnector(type1, start, end, value)
            self.ConnTableRowCount=self.ConnTableRowCount+1
            self.ConnTable.setRowCount(self.ConnTableRowCount)
            self.setConnTableData(self.ConnTableRowCount-1, type1, start, end, value)
            #self.ConnTable.resizeColumnsToContents()
            
    @pyqtSignature("")       
    def on_ConnEditButton_clicked(self):
        if self.ConnTableRowCount==0:
            return
        row=self.ConnTable.currentRow()
        start,end,type1,old_value=self.getConnTableData(row)
        AddEditConnDlg=AddEditConnDialog(type1,old_value,self.syst.n_nodes,start-1,end-1)
        if AddEditConnDlg.exec_():
            type1,start,end,value=AddEditConnDlg.retrieve_data()
            self.syst.addConnector(type1, start, end, value,1,old_value)
            self.setConnTableData(row, type1, start, end, value)
#        print start,end,type1,old_value

    @pyqtSignature("") 
    def on_ConnDelButton_clicked(self):
        if self.ConnTableRowCount==0:
            return
        row=self.ConnTable.currentRow()
        start,end,type1,old_value=self.getConnTableData(row)
        self.syst.addConnector(type1, start-1, end-1, -old_value)
        self.ConnTableRowCount=self.ConnTableRowCount-1
        self.ConnTable.removeRow(row)

    def getConnTableData(self,row):
        start=self.ConnTable.item(row,0).text().toInt()[0]
        end=self.ConnTable.item(row,1).text().toInt()[0]
        type1=1
        if  self.ConnTable.item(row,2).text()=="Spring":
            type1=0
        value=self.ConnTable.item(row,3).text().toFloat()[0]
        return start,end,type1,value
    
    def setConnTableData(self,row,type1,start,end,value):
        self.ConnTable.setItem(row,0,QTableWidgetItem(str(start+1)))
        self.ConnTable.setItem(row,1,QTableWidgetItem(str(end+1)))
        type_string=QString("Spring")
        if type1:
            type_string=QString("Damper")
        self.ConnTable.setItem(row,2,QTableWidgetItem(type_string))
        self.ConnTable.setItem(row,3,QTableWidgetItem(str(value)))
        self.ConnTable.resizeRowsToContents()
    
    def getMassTableData(self,row):
        node=self.MassTable.item(row,0).text().toInt()[0]
        value1=self.MassTable.item(row,1).text().toFloat()[0]
        return node, value1
    
    def setMassTableData(self,row,value1,node):
        self.MassTable.setItem(row,0,QTableWidgetItem(str(node+1)))
        self.MassTable.setItem(row,1,QTableWidgetItem(str(value1)))
        self.MassTable.resizeRowsToContents()
        
    @pyqtSignature("") 
    def on_printSyst_clicked(self):
            print "masses=",self.syst.masses
            print "displacements=",self.syst.displacements
            print "forces=",self.syst.forces
            print "springs=",self.syst.springs
            print "dampers=",self.syst.dampers
            
        
    @pyqtSignature("int")
    def on_nodes_spinBox_valueChanged(self,value):
        print "changed", value
        self.syst.ChangeSize(value)
#        print "masses=",self.syst.masses
#        print "displacements=",self.syst.displacements
#        print "forces=",self.syst.forces
#        print "springs=",self.syst.springs
#        print "dampers=",self.syst.dampers
 
        #if self.n_nodes


class DynSystem:
    def __init__(self):
        self.n_nodes=2
        self.masses=np.zeros((1,self.n_nodes))
        self.springs=np.zeros((self.n_nodes,self.n_nodes))
        self.dampers=np.zeros((self.n_nodes,self.n_nodes))
        self.displacements=[]
        self.forces=[]
        #initArray=[-1 for x in range(0,self.n_nodes)]
        self.displacements,self.forces=[-1 for x in range(0,self.n_nodes)],[-1 for x in range(0,self.n_nodes)]
#        for i in range(0,self.n_nodes):
#            self.displacements.append(0)
#            self.forces.append(0)
    def ChangeSize(self,n_nodes):
        self.masses=np.resize(self.masses,(1,n_nodes))
        if n_nodes>self.n_nodes:
            #Take care of 2D array manipulation
            delta=n_nodes-self.n_nodes
            hor=np.zeros((self.n_nodes,delta))
            ver=np.zeros((delta,n_nodes))
            self.springs=np.vstack((np.hstack((self.springs,hor)),ver))
            self.dampers=np.vstack((np.hstack((self.dampers,hor)),ver))
            # Take care of displacement and forces list
            print self.n_nodes,n_nodes
            for i in range(0,n_nodes-self.n_nodes):
                print i
                self.displacements.append(-1)
                self.forces.append(-1)
            #addArray=[0 for x in range(self.syst.n_nodes,n_nodes)]
        elif n_nodes<self.n_nodes:
            self.springs=np.hsplit(np.vsplit(self.springs,(n_nodes,n_nodes))[0],(n_nodes,n_nodes))[0]
            self.dampers=np.hsplit(np.vsplit(self.dampers,(n_nodes,n_nodes))[0],(n_nodes,n_nodes))[0]
            self.displacements=self.displacements[0:n_nodes]
            self.forces=self.forces[0:n_nodes]
        self.n_nodes=n_nodes
    
    def get_available_mass_nodes(self):
        available_nodes=[]
        print self.displacements
        for i in range(0,len(self.displacements)):
            if (self.displacements[i]==-1) and (self.masses[0][i]==0):
                available_nodes.append(i)
        return available_nodes
    
        
    def addConnector(self,type,start,end,value,edit_flag=0,old_value=0):
        if type==0:
            if edit_flag:
                new_value=value-old_value+self.springs[start][end]
            else:
                new_value=value+self.springs[start][end]
            self.springs[start][end],self.springs[end][start]=new_value,new_value
        else:
            if edit_flag:
                new_value=value-old_value+self.dampers[start][end]
            else:
                new_value=value+self.dampers[start][end]
            self.dampers[start][end],self.dampers[end][start]=new_value,new_value
    
    def addMass(self,node,value1=0,delete_flag=0):
        print node
        if delete_flag:
            self.masses[0][node]=0
        else:
            self.masses[0][node]=value1
            
    def addDisplacement(self,node,value1=0,delete_flag=0):
        if delete_flag:
            self.displacements[node]=-1
        else:
            self.displacements[node]=value1
 
        
class AddEditConnDialog(QDialog,AddEditConnector.Ui_AddConnDialog):
    def __init__(self,type1,value,n_nodes,start=0,end=1,parent=None):
        super(AddEditConnDialog,self).__init__(parent)
        self.setupUi(self)
        self.typeBox.setCurrentIndex(type1)
        for i in range(1,n_nodes+1):
            self.startNode.addItem(str(i))
            self.endNode.addItem(str(i))
        self.editValue.setText(str(value))
        self.startNode.setCurrentIndex(start)
        self.endNode.setCurrentIndex(end)
        
    def accept(self):
        class EqualNodes(Exception):pass
        try:
            if self.startNode.currentIndex()==self.endNode.currentIndex():
                raise EqualNodes, ("Start and End nodes can't be equal")
        except EqualNodes, e:
            QMessageBox.warning(self, "Error:Equal Nodes",unicode(e))
            return

        print "Accepting"
        QDialog.accept(self)
        
    def retrieve_data(self):
            type1=self.typeBox.currentIndex()
            start=self.startNode.currentIndex()
            end=self.endNode.currentIndex()
            value=self.editValue.text().toFloat()[0]
            return type1,start,end,value

class MassDialog(QDialog,MassDlg.Ui_MassDialog):
    def __init__(self,available_nodes,value1=0,current_node=0,parent=None):
        super(MassDialog,self).__init__(parent)
        self.setupUi(self)
        print available_nodes
        for i in available_nodes:
            self.mass_node.addItem(str(i+1))
        self.mass_node.setCurrentIndex(current_node)
        self.mass_value.setText(str(value1))
    def accept(self):
        class MyError(Exception):pass
        try:
            if self.mass_value.text().toFloat()[0]<=0:
                raise MyError, ("Mass can't be negative or zero")
        except MyError, e:
            QMessageBox.warning(self, "Error",unicode(e))
            return

        QDialog.accept(self)
    def retrieve_data(self):
        node=self.mass_node.currentIndex()
        value1=self.mass_value.text().toFloat()[0]
        return node,value1


class CustomFunc:
    def __init__(self,type1=1):
        self.supported={1:'Periodic',2:'Custom'}
        self.type=type1
        self.A=0
        self.B=0
        self.cust=''
        
    def configure(self):
        FunDialog=CustomFuncDlg(self.type,self.A,self.B,self.cust)
        if FunDialog.exec_():
            self.type,self.A,self.B,self.cust=FunDialog.retrieve_data()
            
    def getValue(self,w,t):
        func={1:self.getValuePeriodic,2:self.getValueCustom}
        return func[self.type](w,t)
        
    def getValuePeriodic(self,w,t):
        return self.A*sin(w*t)+self.B*cos(w*t)
    
    def getValueCustom(self,w,t):
        return
    
    def getString(self):
        return {1:str(self.A)+'*sin(w*t)+'+str(self.B)+'*cos(w*t)',2:self.cust}[self.type]
        
 
class CustomFuncDlg(QDialog,FunctionDialog.Ui_FunctionDialog):
    def __init__(self,type,A=0,B=0,cust='',parent=None):
        super(CustomFuncDlg,self).__init__(parent)
        self.setupUi(self)
        self.configure_func={1:self.conf_periodic, 2:self.conf_custom}
        self.configure_func[type](A,B,cust)
        
    def conf_periodic(self,A,B,cust):
        self.editA.setText(str(A))
        self.editB.setText(str(B))
        self.radioButtonPeriodic.setChecked(1)
        
    def conf_custom(self,A,B,cust):
        self.editCustom.setText(str(cust))
        self.radioButtonCustom.setChecked(1)
            
    def retrieve_data(self):
        A=self.editA.text().toFloat()[0]
        B=self.editB.text().toFloat()[0]
        cust=self.editCustom.text()
        type=1
        if self.radioButtonCustom.isChecked():
            type=2
        return type,A,B,cust
    


class Displacement:
    def __init__(self,available_nodes,node=1,funcType=1,movementType=1):
        self.supported={1:'Fixed', 2:'Function'}
        self.supportedMovement={1:'Displacement',2:'Velocity',3:'Acceleration'}
        self.funcType=funcType
        self.movementType=movementType
        self.custFunc=CustomFunc()
        self.node=node

    
    def getValue(self,w,t):
        value_func={1:self.getFixed, 2:self.getFunction}
        return value_func[self.funcType](w,t)
    
    def getFixed(self,w,t):
        return 0
    
    def getFunction(self,w,t):
        return self.custFunc.getValue(w, t)
       
        

    def configure(self,available_nodes,nodeIndex=1):
        DispDialog=DisplacementDlg(nodeIndex,self.custFunc, available_nodes,self.funcType,self.movementType)
        if DispDialog.exec_():
            self.node,self.funcType,self.movementType,self.custFunc=DispDialog.retrieve_data()
            return 1
        return 0
        
          
class DisplacementDlg(QDialog, DisplacementDialog.Ui_Dialog):
    def __init__(self,nodeIndex,custFunc,available_nodes,funcType=1,movementType=1,parent=None):
        super(DisplacementDlg,self).__init__(parent)
        self.setupUi(self)
        self.movementType=movementType
        self.funcType=funcType
        for i in available_nodes:
            self.comboBoxNode.addItem(str(i+1))
        self.comboBoxNode.setCurrentIndex(nodeIndex-1)
#        self.setupUi(self)
#        self.typeFunc={'Fixed':1, 'Custom':2}
#        self.typeIndex={'Displacement':1, 'Velocity':2, 'Acceleration':3}
#        self.func=self.typeFunc[func]
#        self.type=self.typeIndex[type]
        self.configure_func={1:self.conf_fixed, 2:self.conf_custom}
        self.configure_func[funcType]()
        self.customFunc=custFunc
      
    def conf_fixed(self):
        self.radioButtonFixed.setChecked(1)
    
    def conf_custom(self):
        self.radioButtonFunction.setChecked(1)
        self.comboBoxType.setCurrentIndex(self.movementType-1)
    
    @pyqtSignature("")
    def on_buttonDefine_clicked(self):
        self.customFunc.configure()
        
    def retrieve_data(self):
        funcType=1
        if self.radioButtonFunction.isChecked():
            funcType=2
        movementType=self.comboBoxType.currentIndex()+1
        node=self.comboBoxNode.currentIndex()
        return node,funcType,movementType,self.customFunc

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    form=MainDlg()
    form.show()
    app.exec_()
    