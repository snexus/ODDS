'''
Created on Dec 30, 2011

@author: Denis Lepchev
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import AddEditConnector
import MassDlg
import oddsFormMain
import FunctionDialog
import DisplacementDialog
import ForceDialog
from math import *
from scipy.integrate import odeint
from scipy.integrate import trapz
from scipy.linalg import eig
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#import res_explorer
import time
from res_explorer import ResultExplorer
from scipy import interpolate
import pickle

class MainWindow(QMainWindow,oddsFormMain.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.syst=DynSystem()
        self.nodes_spinBox.setValue(self.syst.n_nodes)
        self.nodes_spinBox.setMinimum(2)
        self.ResExplorer=ResultExplorer()
 
        #initialize tables
        self.ConnTableRowCount,self.MassTableRowCount,self.DispTableRowCount,self.ForceTableRowCount=0,0,0,0
        self.initTables([self.ConnTable,self.MassTable,self.DispTable,self.ForceTable,self.tableWidgetInitCon])
        
        self.connect(self.actionSave, SIGNAL("triggered()"), self.fileSave)
        self.connect(self.actionOpen, SIGNAL("triggered()"), self.fileOpen)
        self.comboBoxPeaks.setCurrentIndex(1)

    def fileSave(self):
        fname = unicode(QFileDialog.getSaveFileName(self,"ODDS - Choose File Name", "system.ods","ODDS files (*.ods);;All files (*.* *)"))
        if fname=="":
            return
        try:
            pickle.dump(self.syst, open(fname, 'wb'))
        except:
            QMessageBox.warning(self, "Error","File was not saved")

    def fileOpen(self):
        fname = unicode(QFileDialog.getOpenFileName(self,"ODDS - Choose File Name", "","ODDS files (*.ods);;All files (*.* *)"))
        if fname=="":
            return
        try:
            self.syst=pickle.load(file(fname))
            self.update_interface()
        except:
            QMessageBox.warning(self, "Error","File was not opened")

    
    
    def initTables(self,tables):
        for table in tables:
            table.setAlternatingRowColors(True)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setSelectionMode(QTableWidget.SingleSelection)
    
    
    #def on_lineEdit_DispInit_returnPressed(self):
    @pyqtSignature("QString")
    def on_lineEdit_DispInit_textEdited(self,string1):
        #print "changed, displ"
        self.SetInit()
#        print "\n Displacement DOF 0"
#        print self.syst.initDisp[0][self.syst.DOF[0]]
#        print "\n Displacement DOF 1"
#        print self.syst.initDisp[0][self.syst.DOF[1]]

        
    #def on_lineEdit_VelInit_returnPressed(self):
    @pyqtSignature("QString")
    def on_lineEdit_VelInit_textEdited(self,string1):
        self.SetInit()
#        print "\n Velocity DOF 0"
#        print self.syst.initVel[0][self.syst.DOF[0]]
#        print "\n Velocity DOF 1"
#        print self.syst.initVel[0][self.syst.DOF[1]]
    
    @pyqtSignature("int")
    def on_tabWidget_currentChanged(self,index):
        if index==1:
            self.syst.prepare_system()
            if len(self.syst.DOF)==0:
                return
            self.comboBox_DOF.clear()
            for i in self.syst.DOF:
                self.comboBox_DOF.addItem(str(i+1))
            self.update_init_cond_list()
            self.on_comboBox_DOF_currentIndexChanged(0)
    
    @pyqtSignature("int")
    def on_comboBox_DOF_currentIndexChanged(self,index):
#        print "\n changing Displacement DOF 0"
#        print self.syst.initDisp[0][self.syst.DOF[0]]
#        print "\n Changing Displacement DOF 1"
#        print self.syst.initDisp[0][self.syst.DOF[1]]
#        print "\n Changing Velocity DOF 0"
#        print self.syst.initVel[0][self.syst.DOF[0]]
#        print "\n Changing Velocity DOF 1"
#        print self.syst.initVel[0][self.syst.DOF[1]]
        currentDOF=index
        self.lineEdit_DispInit.setText(str(self.syst.initDisp[0][self.syst.DOF[currentDOF]]))
        self.lineEdit_VelInit.setText(str(self.syst.initVel[0][self.syst.DOF[currentDOF]]))
        
        
    @pyqtSignature("")
    def SetInit(self):
        currentDOF=self.comboBox_DOF.currentIndex()
        Disp=self.lineEdit_DispInit.text().toFloat()[0]
        Vel=self.lineEdit_VelInit.text().toFloat()[0]
        self.syst.initDisp[0][self.syst.DOF[currentDOF]]=Disp
        self.syst.initVel[0][self.syst.DOF[currentDOF]]=Vel
        self.update_init_cond_list()
        
        
        
        
    def update_init_cond_list(self):
        length=len(self.syst.DOF)
        self.tableWidgetInitCon.clearContents()
        self.tableWidgetInitCon.setRowCount(length)
        for i in range(0,length):
            print i, self.syst.DOF[i],
            self.tableWidgetInitCon.setItem(i,0,QTableWidgetItem(str(self.syst.DOF[i]+1)))
            self.tableWidgetInitCon.setItem(i,1,QTableWidgetItem(str(self.syst.initDisp[0][self.syst.DOF[i]])))
            self.tableWidgetInitCon.setItem(i,2,QTableWidgetItem(str(self.syst.initVel[0][self.syst.DOF[i]])))
        self.tableWidgetInitCon.resizeColumnsToContents()
        self.tableWidgetInitCon.resizeRowsToContents()
        
        
        
    @pyqtSignature("")
    def on_pushButton_Solve_clicked(self):
        #self.syst.prepare_system()
        self.ResExplorer.clear()
        Npoints,res=0,0
        Npeaks=self.lineEdit_Npeaks.text().toFloat()[0]
        NpeaskSS=self.lineEdit_NpeaksSS.text().toFloat()[0]
        init_con=self.syst.form_init_conditions()
        print init_con
        #init_con=[0]*len(self.syst.DOF)*2
        if self.radioButton_constantNpeak.isChecked():
            Npoints=self.lineEdit_constNpeak.text().toFloat()[0]
        else:
            N=self.lineEdit_varNpeak.text().toFloat()[0]
            if N!=0:
                res=1.0/N
        if self.radioButton_SingleFreq.isChecked():
            start_time=self.lineStartTime.text().toFloat()[0]
            freq=self.lineEdit_SingleFreq.text().toFloat()[0]
            if self.comboBoxPeaks.currentIndex()==1:
                Npeaks=Npeaks*freq
            self.syst.form_displacement_functions(Npeaks/freq,freq,10000,start_time)
            t,result=self.syst.solve_for_frequency(freq,init_con,Npeaks,Npoints,res,start_time)
            self.syst.find_natural_frequencies()
            for i in range(0,len(self.syst.DOF)):
                self.ResExplorer.add_result("Displacement - node #"+str(self.syst.DOF[i]), t, result[i*2], "Time [sec]", "Displacement")
                self.ResExplorer.add_result("Velocity - node # "+str(self.syst.DOF[i]), t, result[i*2+1], "Time [sec]", "Velocity")
                self.ResExplorer.add_custom_text("Undamped frequency Wn"+str(i)+" = "+str(self.syst.nat_freq[i]))
                self.ResExplorer.add_custom_text("Undamped mode shape M"+str(i)+" = "+str(self.syst.mode_shapes[i]))
                
            
            for i in range(0,len(self.syst.displacements)):
                if self.syst.displacements[i]!=-1:
                    vel_base,disp_base=[],[]
                    for time in t:
                        xj,vj=self.syst.displacements[i].getValue(freq*2*pi,time)
                        disp_base.append(xj);vel_base.append(vj)
                    self.ResExplorer.add_result("Displacement (base) - node #"+str(i), t, disp_base, "Time [sec]", "Displacement")
                    self.ResExplorer.add_result("Velocity (base) - node #"+str(i), t, vel_base, "Time [sec]", "Velocity")
            self.syst.find_natural_frequencies()
         
                
            
            
#            plt.figure()
#            plt.plot(t,result[0])
#            plt.show()
        else:
            start=self.lineEdit_FreqStart.text().toFloat()[0]
            stop=self.lineEdit_FreqStop.text().toFloat()[0]
            step=self.lineEdit_FreqStep.text().toFloat()[0]
            frequency,response=self.syst.frequency_sweep(start,stop,step,self.progressBar_Solution,NpeaskSS,Npeaks,Npoints,res)
            for i in range(0,len(self.syst.DOF)):
                self.ResExplorer.add_result("Displacement - node #"+str(self.syst.DOF[i]), frequency, response[i*2], "Frequency [Hz]", "Displacement")
                self.ResExplorer.add_result("Velocity - node # "+str(self.syst.DOF[i]), frequency, response[i*2+1], "Frequency [Hz]", "Velocity")
#            
#            plt.figure()
#            plt.plot(frequency,response[0])
#            plt.show()
        self.ResExplorer.set_default_result(0)
        self.ResExplorer.show()
            
        
    @pyqtSignature("")
    def on_testODE_clicked(self):
        pickle.dump(self.syst, open('system.out', 'wb'))
        self.syst.omega=5
        print "A =",self.syst.omega
        self.syst=pickle.load(file("system.out"))
        print "B=",self.syst.omega


    @pyqtSignature("")
    def on_modeDecomp_clicked(self):
        self.syst.prepare_system()
        print "\nM matrix = ",self.syst.K_matrix
        print "\nK matrix = ",self.syst.M_matrix
        print "\nF matrix = ",self.syst.Fcoeff_matrix
        self.syst.mode_decomp_transform_matrix()
        init_con=self.syst.form_init_conditions_mode_decomp()
        print "\nInitial conditions =",init_con
        self.ResExplorer.clear()
        Npoints,res=0,0
        Npeaks=self.lineEdit_Npeaks.text().toFloat()[0]
        NpeaskSS=self.lineEdit_NpeaksSS.text().toFloat()[0]
        if self.radioButton_constantNpeak.isChecked():
            Npoints=self.lineEdit_constNpeak.text().toFloat()[0]
        else:
            N=self.lineEdit_varNpeak.text().toFloat()[0]
            if N!=0:
                res=1.0/N
        start_time=self.lineStartTime.text().toFloat()[0]
        freq=self.lineEdit_SingleFreq.text().toFloat()[0]
        if self.comboBoxPeaks.currentIndex()==1:
            Npeaks=Npeaks*freq
        self.syst.form_displacement_functions(Npeaks/freq,freq,10000,start_time)
        t,result=self.syst.solve_for_frequency_mode_decomp(freq,init_con,Npeaks,Npoints,res,start_time)
        print result
        
    
    @pyqtSignature("")
    def on_ForceAddButton_clicked(self):
        available_nodes=self.syst.get_available_force_nodes()
        if len(available_nodes)==0:
            QMessageBox.warning(self, "Error","Define masses first")
            return
        F=Force()
        if F.configure(available_nodes):
            self.syst.addForce(available_nodes[F.node],F)
            self.ForceTableRowCount=self.ForceTableRowCount+1
            self.ForceTable.setRowCount(self.ForceTableRowCount)
            self.setForceTableData(self.ForceTableRowCount-1,F,available_nodes[F.node])
            
    
    
    
    
    def update_interface(self):
        tables=[self.ConnTable,self.MassTable,self.DispTable,self.ForceTable,self.tableWidgetInitCon]  
        for table in tables:
            table.clearContents()
            table.update()
        m_row,f_row,d_row,c_row=1,1,1,1
        self.ConnTableRowCount,self.MassTableRowCount,self.DispTableRowCount,self.ForceTableRowCount=0,0,0,0
        for i in range(0,self.syst.n_nodes):
            c_mass=self.syst.masses[0][i]
            c_disp=self.syst.displacements[i]
            c_force=self.syst.forces[i]
            if c_mass!=0:
                self.MassTable.setRowCount(m_row)
                self.setMassTableData(m_row-1,c_mass,i)
                m_row=m_row+1
            if c_disp!=-1:
                self.DispTable.setRowCount(d_row)
                self.setDispTableData(d_row-1, c_disp, i)
                d_row=d_row+1
            if c_force!=-1:
                self.ForceTable.setRowCount(f_row)
                self.setForceTableData(f_row-1, c_force, i)
                f_row=f_row+1
            for j in range(i+1,self.syst.n_nodes):
                if self.syst.springs[i][j]!=0:
                    self.ConnTable.setRowCount(c_row)
                    self.setConnTableData(c_row-1, 0, i, j, self.syst.springs[i][j])
                    c_row=c_row+1
                if self.syst.dampers[i][j]!=0:
                    self.ConnTable.setRowCount(c_row)
                    self.setConnTableData(c_row-1, 1, i, j, self.syst.dampers[i][j])
                    c_row=c_row+1
        self.ConnTableRowCount,self.MassTableRowCount,self.DispTableRowCount,self.ForceTableRowCount=c_row-1,m_row-1,d_row-1,f_row-1  
                
        
    @pyqtSignature("")
    def on_ForceEditButton_clicked(self):
        if self.ForceTable.hasFocus():
            if self.ForceTableRowCount==0:
                return
        row=self.ForceTable.currentRow()
        node=self.ForceTable.item(row,0).text().toInt()[0]
        available_nodes=self.syst.get_available_force_nodes()
        available_nodes.append(node-1)
        available_nodes.sort()
        F=self.syst.forces[node-1]
        if F.configure(available_nodes,available_nodes.index(node-1)+1):
            self.syst.addForce(node-1, delete_flag=1)
            self.syst.addForce(available_nodes[F.node], F)
            self.setForceTableData(row, F,available_nodes[F.node])
        
    @pyqtSignature("")
    def on_ForceDeleteButton_clicked(self):
        if self.ForceTable.hasFocus():
            if self.ForceTableRowCount==0:
                return
            row=self.ForceTable.currentRow()
            node=self.ForceTable.item(row,0).text().toInt()[0]
            self.syst.addForce(node-1,delete_flag=1)
            self.ForceTableRowCount=self.ForceTableRowCount-1
            self.ForceTable.removeRow(row)
        else:
            QMessageBox.information(self, "Note","Please select item at force table")
    
    @pyqtSignature("")
    def on_DispAddButton_clicked(self):
        available_nodes=self.syst.get_available_mass_nodes()
        if len(available_nodes)==0:
            QMessageBox.warning(self, "Error","No more available nodes for displacements")
            return
        Disp=Displacement(available_nodes)
        if Disp.configure(available_nodes):
            print Disp.node
            self.syst.addDisplacement(available_nodes[Disp.node], Disp)
            self.DispTableRowCount=self.DispTableRowCount+1
            self.DispTable.setRowCount(self.DispTableRowCount)
            self.setDispTableData(self.DispTableRowCount-1, Disp,available_nodes[Disp.node])
    
    def setForceTableData(self,row,F,node):
        func=F.custFunc.supported[F.custFunc.type]
        value=F.custFunc.getString()
        self.ForceTable.setItem(row,0,QTableWidgetItem(str(node+1)))
        self.ForceTable.setItem(row,1,QTableWidgetItem(func))
        self.ForceTable.setItem(row,2,QTableWidgetItem(value))
        self.ForceTable.resizeColumnsToContents()
        self.ForceTable.resizeRowsToContents()
    
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
        self.syst.find_natural_frequencies()
        nat_freq,masses=[],[]
        if len(self.syst.DOF)>0:
            nat_freq,masses=self.syst.nat_freq, self.syst.masses[0][self.syst.DOF]
        AddEditConnDlg=AddEditConnDialog(0,0,self.syst.n_nodes,nat_freq,masses)
        if AddEditConnDlg.exec_():
            type1,start,end,value=AddEditConnDlg.retrieve_data()
            self.syst.addConnector(type1, start, end, value)
            self.ConnTableRowCount=self.ConnTableRowCount+1
            self.ConnTable.setRowCount(self.ConnTableRowCount)
            self.setConnTableData(self.ConnTableRowCount-1, type1, start, end, value)
            #self.ConnTable.resizeColumnsToContents()
            
    @pyqtSignature("")       
    def on_ConnEditButton_clicked(self):
        if self.ConnTable.hasFocus():
            if self.ConnTableRowCount==0:
                return
            row=self.ConnTable.currentRow()
            start,end,type1,old_value=self.getConnTableData(row)
            self.syst.find_natural_frequencies()
            nat_freq,masses=[],[]
            if len(self.syst.DOF)>0:
                nat_freq,masses=self.syst.nat_freq, self.syst.masses[0][self.syst.DOF]
            AddEditConnDlg=AddEditConnDialog(type1,old_value,self.syst.n_nodes,nat_freq,masses,start-1,end-1)
            old_type,old_start,old_end=type1,start,end
            if AddEditConnDlg.exec_():
                type1,start,end,value=AddEditConnDlg.retrieve_data()
                if old_type!=type1:
                    self.syst.addConnector(old_type, old_start-1, old_end-1, 0,1,old_value)
                    self.syst.addConnector(type1, start, end, value,0,old_value)
                else:
                    self.syst.addConnector(type1, start, end, value,1,old_value)
                self.setConnTableData(row, type1, start, end, value)
#        print start,end,type1,old_value

    @pyqtSignature("") 
    def on_ConnDelButton_clicked(self):
        if self.ConnTable.hasFocus():
            if self.ConnTableRowCount==0:
                return
            row=self.ConnTable.currentRow()
            start,end,type1,old_value=self.getConnTableData(row)
            self.syst.addConnector(type1, start-1, end-1, -old_value)
            self.ConnTableRowCount=self.ConnTableRowCount-1
            self.ConnTable.removeRow(row)
        else:
            QMessageBox.information(self, "Note","Please select item from connection table")

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
            print "initDisp",self.syst.initDisp
            print "initVel",self.syst.initVel
            self.syst.find_natural_frequencies()
            print "K_matrix",self.syst.K_matrix
            print "M_matrix",self.syst.M_matrix
            
        
    @pyqtSignature("int")
    def on_nodes_spinBox_valueChanged(self,value):
        self.syst.ChangeSize(value)
        self.update_interface()


class DynSystem:
    def __init__(self):
        self.n_nodes=2
        self.masses=np.zeros((1,self.n_nodes))
        self.initDisp=np.zeros((1,self.n_nodes))
        self.initVel=np.zeros((1,self.n_nodes))
        self.springs=np.zeros((self.n_nodes,self.n_nodes))
        self.dampers=np.zeros((self.n_nodes,self.n_nodes))
        self.zeta=np.zeros
        self.displacements=[]
        self.forces=[]
        self.DOF=[]
        self.omega=50.0
        #initArray=[-1 for x in range(0,self.n_nodes)]
        self.displacements,self.forces=[-1 for x in range(0,self.n_nodes)],[-1 for x in range(0,self.n_nodes)]
        self.nat_freq=[]
        self.mode_shapes=[]
#        for i in range(0,self.n_nodes):
#            self.displacements.append(0)
#            self.forces.append(0)
    def form_init_conditions(self):
        init_con=[]
        for i in self.DOF:
            init_con.append(self.initDisp[0][i])
            init_con.append(self.initVel[0][i])
        return init_con
            
    def form_displacement_functions(self,endtime,w,num_points,start_time=0.0):
        for disp in self.displacements:
            if disp!=-1:
                if disp.custFunc.type==2:
                    disp.FormVelocityDisplacement_custom(endtime,start_time,w,num_points)
    
    def ode_system(self,w,t):
        f,counter=[],0
        for i in self.DOF:
            xi,vi=w[counter],w[counter+1]
            counter=counter+2
            f.append(vi)
            Force,SpringForce,DamperForce=0.0,0.0,0.0
            if self.forces[i]!=-1:
                Force=self.forces[i].getValue(self.omega,t)
                #print t, Force
            for j in range(0,self.Length):
                if j!=i:
                    if j in self.DOF:
                        xj,vj=w[self.DOF.index(j)*2],w[self.DOF.index(j)*2+1]
                    else:
                        xj,vj=self.displacements[j].getValue(self.omega,t)
                    SpringForce=SpringForce+self.springs[i][j]*(xi-xj)
                    DamperForce=DamperForce+self.dampers[i][j]*(vi-vj)
            xi_tag=(Force-SpringForce-DamperForce)/self.masses[0][i]
            f.append(xi_tag)
        return f
    
    def mode_decomp_solver(self,w,t):
        f,counter=[],0
        sizeFcoeff=self.Fcoeff_matrix.shape
        ForceVector=np.zeros((len(self.DOF),1))
#        print "Force Vectr = ",ForceVector
#        print "FcoeffMatrix = ",self.Fcoeff_matrix
        #for i in range(0,sizeFcoeff[0]):
        for i in self.DOF:
            ind_i=self.DOF.index(i)
            print "i, ind_i =",i,ind_i
            Force=0.0
            if self.forces[i]!=-1:
                Force=self.forces[i].getValue(self.omega,t)
            ForceVector[ind_i]=ForceVector[ind_i]+Force
            for j in range(0,sizeFcoeff[1]):            
                xj=0.0
                if hasattr(self.displacements[j], "getValue"):
                    xj,vj=self.displacements[j].getValue(self.omega,t)
                ForceVector[ind_i]=ForceVector[ind_i]+self.Fcoeff_matrix[ind_i][j]*xj
        TransformedForce=np.dot(self.Transf_matrix.T,ForceVector)
        for i,k in zip(self.DOF,range(0,len(self.DOF))):
            xi,vi=w[counter],w[counter+1]
            counter=counter+2
            f.append(vi)
            f.append(TransformedForce[k]-2*self.zeta[k]*self.nat_freq[k]*vi-(self.nat_freq[k]**2)*xi)
        print "f=",f
        return f
       
    
    def form_KM_matrix(self):
        self.K_matrix=np.zeros((len(self.DOF),len(self.DOF)))
        self.M_matrix=np.zeros((len(self.DOF),len(self.DOF)))
        Length=len(self.displacements)
        self.Fcoeff_matrix=np.zeros((len(self.DOF),Length))
        #print self.DOF
        for i in self.DOF:
            ind_i=self.DOF.index(i)
            self.M_matrix[ind_i][ind_i]=self.masses[0][i]
            for j in range(0,Length):
                self.K_matrix[ind_i][ind_i]=self.K_matrix[ind_i][ind_i]+self.springs[i][j]
                if j in self.DOF:
                    ind_j=self.DOF.index(j)
                    self.K_matrix[ind_i][ind_j]=self.K_matrix[ind_i][ind_j]-self.springs[i][j]
                else:
                    self.Fcoeff_matrix[ind_i][j]=self.springs[i][j]
                
    def mode_decomp_transform_matrix(self):
        Kmat=self.K_matrix     
        Mmat=self.M_matrix
#        print "Kmat = ",Kmat
#        print "Mmat = ",Mmat
        w,v=eig(Kmat,Mmat,left=True,right=False)
        self.nat_freq=np.real(np.sqrt(w))
        self.omega
        print "v,w= ",v,w
        v=v.T
        v1=v[0][np.newaxis]
#        print "v1= ",v1
#        print "multiply = ",sqrt(1.0/np.dot(np.dot(v1,Mmat),v1.T))
        r1=sqrt(1.0/np.dot(np.dot(v1,Mmat),v1.T))
        self.Transf_matrix=r1*v1
        for i in range(1,v.shape[1]):
            v1=v[i][np.newaxis]
            r1=sqrt(1.0/np.dot(np.dot(v1,Mmat),v1.T))
            self.Transf_matrix=np.concatenate((self.Transf_matrix,r1*v1),axis=0).T
        print "\nTransformation matrix = \n",self.Transf_matrix       
        
    def form_init_conditions_mode_decomp(self):
        init_con=[]
        init_disp=np.array([self.initDisp[0][i] for i in self.DOF])
        init_vel=np.array([self.initVel[0][i] for i in self.DOF])
        trans_disp=np.dot(np.dot(self.Transf_matrix.T,self.M_matrix),init_disp)
        trans_vel=np.dot(np.dot(self.Transf_matrix.T,self.M_matrix),init_vel)
        for i in range(0,len(trans_disp)):
            init_con.append(trans_disp[i])
            init_con.append(trans_vel[i])
        return init_con
    
    def find_natural_frequencies(self):
        self.prepare_system()
        if len(self.DOF)==0:
            return
        print self.K_matrix,self.M_matrix
        
        w,v=eig(self.K_matrix,self.M_matrix)
        self.nat_freq=np.real(np.sqrt(w))
        self.mode_shapes=np.real(v).T
        print self.nat_freq
        print self.mode_shapes
        
    def prepare_system(self):
# calculate degrees of Freedom of system
        self.DOF=[]      
        self.Length=len(self.displacements)
        #self.init_con=[0]*len(self.DOF)
        for i in range(0,self.Length):
            if (self.masses[0][i]!=0):
                self.DOF.append(i)
                #self.initDisp.append(0)
                #self.initVel.append(0)
        self.form_KM_matrix()
        print "DOF=",self.DOF
        self.zeta=np.zeros(len(self.DOF))
        #print(self.displacements[0].getValue(15,2))
        
    def solve_for_frequency(self, freq,init_conditions,n_peaks=10.0,npoints_peak=500.0,resolution=0.1,start_time=0.0):
        
        self.omega=freq*2*pi
        stop_time=n_peaks/freq
        if npoints_peak==0:
            num_points=freq/resolution*n_peaks
        else:
            num_points=npoints_peak*n_peaks
        t=np.linspace(start_time,stop_time,num_points)
        result=odeint(self.ode_system,init_conditions,t).T
        return t,result
    
    def solve_for_frequency_mode_decomp(self, freq,init_conditions,n_peaks=10.0,npoints_peak=500.0,resolution=0.1,start_time=0.0):
        
        self.omega=freq*2*pi
        stop_time=n_peaks/freq
        if npoints_peak==0:
            num_points=freq/resolution*n_peaks
        else:
            num_points=npoints_peak*n_peaks
        t=np.linspace(start_time,stop_time,num_points)
        result=odeint(self.mode_decomp_solver,init_conditions,t).T
        return t,result
    
    
    def frequency_sweep(self,start_freq,end_freq,freq_step,progressbar,NpeaksSS=2.0,n_peaks=10.0,npoints_peak=500.0,resolution=0.1,seek_steady_state=0):
 #       self.prepare_system()
        init_con=[0]*len(self.DOF)*2
    #    resolution=0.1
        freq_sweep=np.arange(start_freq,end_freq,freq_step)
        if npoints_peak==0:
            num_points_peak=freq_sweep/resolution
        else:
            num_points_peak=np.array([npoints_peak]*len(freq_sweep))
        stop_time=n_peaks/freq_sweep
        seek_time=(n_peaks-NpeaksSS)*num_points_peak.round() # for damped systems
        #seek_time=[0]*len(freq_sweep) # for undamped systems
        omega=freq_sweep*2*pi
        response=[]
        for i in range(0,len(self.DOF)*2):
            response.append([])
        
        Tstart = time.time()
        progressbar.setMinimum(0)
        progressbar.setMaximum(len(freq_sweep))
        progressbar.reset()
        for ind,freq in zip(range(0,len(freq_sweep)),freq_sweep):
            self.form_displacement_functions(n_peaks/freq,freq,10000)
            t=np.linspace(0,stop_time[ind],num_points_peak[ind]*n_peaks)
            self.omega=omega[ind]
            result=odeint(self.ode_system,init_con,t).T
            progressbar.setValue(ind)
            for i in range(0,len(self.DOF)):
                #response.append([])
                max_disp_resp=max(abs(result[i*2][seek_time[ind]:]))
                max_vel_resp=max(abs(result[i*2+1][seek_time[ind]:]))
                response[i*2].append(max_disp_resp)
                response[i*2+1].append(max_vel_resp)
                
        print time.time() - Tstart
        return freq_sweep,response
            
         
#    def frequency_sweep(self,start_freq,end_freq,freq_step,n_peaks=10.0,npoints_peak=500.0,seek_steady_state=0):
#        self.prepare_system()
#        init_con=[0]*len(self.DOF)*2
#        freq_sweep=np.arange(start_freq,end_freq,freq_step)
#        
#        resolution=0.1
#        response=[]
#        Tstart = time.time()
#        for freq in freq_sweep:
#            num_points_peak=freq/resolution
#            stop_time=n_peaks/freq
#            t=np.linspace(0,stop_time,num_points_peak*n_peaks)
#            seek_time=int((n_peaks-2)*num_points_peak)
#            self.omega=freq*2*pi
#            wsol=odeint(self.ode_system,init_con,t)
#            result=np.array(wsol).T
#            #t,result=self.solve_for_frequency(freq,init_con,n_peaks,npoints_peak)
#            for i in range(0,len(self.DOF)):
#                response.append([])
#                max_disp_resp=max(abs(result[i*2][seek_time:]))
#                response[i].append(max_disp_resp)
#        print time.time() - Tstart
#        return freq_sweep,response   

    def ChangeSize(self,n_nodes):
        self.masses.resize((1,n_nodes),refcheck=False)
        #self.masses=np.resize(self.masses,(1,n_nodes))
        #self.masses[0][-1] #bug in resize??
        self.initDisp.resize((1,n_nodes),refcheck=False)
        self.initVel.resize((1,n_nodes),refcheck=False)
        #self.initDisp=np.resize(self.initDisp,(1,n_nodes))
        #self.initVel=np.resize(self.initVel,(1,n_nodes))
        

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
                #print i
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
        for i in range(0,len(self.displacements)):
            if (self.displacements[i]==-1) and (self.masses[0][i]==0):
                available_nodes.append(i)
        return available_nodes
    
    def get_available_force_nodes(self):
        available_nodes=[]
        for i in range(0,len(self.displacements)):
            if (self.masses[0][i]>0) and (self.forces[i]==-1):
                available_nodes.append(i)
        return available_nodes
    
    def addForce(self,node,value1=0,delete_flag=0):
        if delete_flag:
            self.forces[node]=-1
        else:
            self.forces[node]=value1
    
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
            self.initDisp[0][node]=0
            self.initVel[0][node]=0
        else:
            self.masses[0][node]=value1
            
    def addDisplacement(self,node,value1=0,delete_flag=0):
        if delete_flag:
            self.displacements[node]=-1
        else:
            self.displacements[node]=value1
 
        
class AddEditConnDialog(QDialog,AddEditConnector.Ui_AddConnDialog):
    def __init__(self,type1,value,n_nodes,nat_freq=[],masses=[],start=0,end=1,parent=None):
        super(AddEditConnDialog,self).__init__(parent)
        self.setupUi(self)
        self.typeBox.setCurrentIndex(type1)
        for i in range(1,n_nodes+1):
            self.startNode.addItem(str(i))
            self.endNode.addItem(str(i))
        self.editValue.setText(str(value))
        self.startNode.setCurrentIndex(start)
        self.endNode.setCurrentIndex(end)
        self.nat_freq=nat_freq
        self.masses=masses
    
    @pyqtSignature("int")
    def on_typeBox_currentIndexChanged(self,index):
        if index==1:
            self.modalDamping_edit.setEnabled(True)
            self.modalDamping_pushbutton.setEnabled(True)
            self.label_5.setEnabled(True)
        else:
            self.modalDamping_edit.setEnabled(False)
            self.modalDamping_pushbutton.setEnabled(False)
            self.label_5.setEnabled(False)
    
    @pyqtSignature("")
    def on_modalDamping_pushbutton_clicked(self):
        #print "here"
        modal_ratio=self.modalDamping_edit.text().toFloat()[0]
        if len(self.nat_freq)==0:
            QMessageBox.warning(self, "Error: Can't find undamped natural frequncies","Please define undamped system first")
            return
        else:
            pass
        #message="kukareku\nmuhaha"

    #QTimer.singleShot(60000, app.quit) # 1 minute
        string=""
        for freq,mass, in zip(self.nat_freq,self.masses):
            string+="C= "+str(modal_ratio*2*mass*freq)+"\n"
        QMessageBox.information(self, "Damping ratios:",string)
        
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
        self.custom_functions,self.custom_times=[],[0]
        self.cust=''
        self.InterpStep=0.01
        
    def configure(self):
        FunDialog=CustomFuncDlg(self.type,self.A,self.B,self.custom_functions,self.custom_times,self.InterpStep)
        if FunDialog.exec_():
            self.type,self.A,self.B,self.custom_functions,self.custom_times,self.InterpStep=FunDialog.retrieve_data()
            return 1
        return 0
            
    def getValue(self,w,t):
        func={1:self.getValuePeriodic,2:self.getValueCustom}
        return func[self.type](w,t)
        
    def getValuePeriodic(self,w,t):
        return self.A*sin(w*t)+self.B*cos(w*t)
    
    def getValueCustom(self,w,t):
        print t,self.custom_functions,self.custom_times,np.nonzero(np.array(self.custom_times)<=t)
        function_index=np.nonzero(np.array(self.custom_times)<=t)[0][-1]
        #print t, eval(self.custom_functions[function_index])
        return eval(self.custom_functions[function_index])
    
    def getString(self):
        strA,strB,oper=str(self.A)+'*sin(w*t)','',''
        if self.B!=0:
            oper='+'
            strB=str(self.B)+'*cos(w*t)'
        if self.A==0:
            strA=''
            oper=''
        return {1:strA+oper+strB,2:"Custom"}[self.type]
        
 
class CustomFuncDlg(QDialog,FunctionDialog.Ui_FunctionDialog):
    def __init__(self,type,A=0,B=0,custom_functions=[],custom_times=[0],InterpStep=0.01,parent=None):
        super(CustomFuncDlg,self).__init__(parent)
        self.setupUi(self)
        self.custom_functions=custom_functions
        self.custom_times=custom_times
        self.configure_func={1:self.conf_periodic, 2:self.conf_custom}
        self.configure_func[type](A,B,custom_functions,custom_times,InterpStep)

        
    def conf_periodic(self,A,B,custom_functions,custom_times,InterpStep):
        self.editA.setText(str(A))
        self.editB.setText(str(B))
        self.radioButtonPeriodic.setChecked(1)
    
    
    def accept(self):
        if self.radioButtonCustom.isChecked():
            if not len(self.custom_functions):
                QMessageBox.warning(self, "Error","Please define at least one step for custom function")
                return
        QDialog.accept(self)
        
    @pyqtSignature("")
    def on_addStep_clicked(self):
        endTime=self.endTimeEdit.text().toFloat()[0]
        custFunc=str(self.editCustom.text())
        w,t=1.0,1.0
        try:
            a=eval(custFunc)
            print a
        except:
            QMessageBox.warning(self, "Error","Please enter a valid function that depends on w or/and t only")
            return
        if endTime<=self.custom_times[-1]:
            QMessageBox.warning(self, "Error","Please enter time greater than "+str(self.custom_times[-1])+" sec.")
            return
        time_step=self.EditInterpStep.text().toFloat()[0]
        current_step=abs(endTime-self.custom_times[-1])
        step=min(time_step*100.0,current_step)
        self.EditInterpStep.setText(str(step/100.0))
        self.custom_times.append(endTime)
        self.startTimeLabel.setText(str(self.custom_times[-1]))
        self.custom_functions.append(custFunc)
        self.update_custom_f_table()
    
    @pyqtSignature("")
    def on_deleteStep_clicked(self):
        if len(self.custom_functions)>0:
            self.custom_functions.pop()
            self.custom_times.pop()
            self.update_custom_f_table()
    
    def update_custom_f_table(self):
        self.TableCustomFunc.clearContents()
        self.TableCustomFunc.update()
        length=len(self.custom_functions)
        if length>0:
            self.TableCustomFunc.setRowCount(length)
            for i in range(0,length):
                    self.TableCustomFunc.setItem(i,0,QTableWidgetItem(str(self.custom_times[i])))
                    self.TableCustomFunc.setItem(i,1,QTableWidgetItem(str(self.custom_times[i+1])))
                    self.TableCustomFunc.setItem(i,2,QTableWidgetItem(str(self.custom_functions[i])))
            self.TableCustomFunc.resizeColumnsToContents()
            self.TableCustomFunc.resizeRowsToContents()
                
        
    def conf_custom(self,A,B,custom_functions,custom_times,InterpStep):
        #self.editCustom.setText(str(cust))
        self.update_custom_f_table()
        self.EditInterpStep.setText(str(InterpStep))
        self.radioButtonCustom.setChecked(1)
            
    def retrieve_data(self):
        A=self.editA.text().toFloat()[0]
        B=self.editB.text().toFloat()[0]
        InterpStep=self.EditInterpStep.text().toFloat()[0]
        type1=1
        if self.radioButtonCustom.isChecked():
            type1=2
        return type1,A,B,self.custom_functions,self.custom_times,InterpStep
    
    @pyqtSignature("")
    def on_ShowInterp_Button_clicked(self):
        time_step=self.EditInterpStep.text().toFloat()[0]
        endTime=self.custom_times[-1]
        npoints=int(endTime/time_step)
        time=np.linspace(0.0,endTime,npoints)[0:-1]
        #print endTime,npoints,time
        #print self.custom_functions
        vec=[]
        for t in time:
            function_index=np.nonzero(np.array(self.custom_times)<=t)[0][-1]
            print function_index
            vec.append(eval(self.custom_functions[function_index]))
        interpolated=interpolate.splrep(time,vec,s=0)
        plt.figure()
        plt.plot(time,vec)
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("Interpolated function with step= "+str(time_step))
        plt.grid(True)
        text=self.ShowInterp_Button.text()
        if text=='Show':
            self.ShowInterp_Button.setText("Hide")
            plt.show()
        else:
            self.ShowInterp_Button.setText("Show")
            plt.close('all')

        

        

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
        return 0,0
    
    def FormVelocityDisplacement_custom(self,endTime,start_time=0.0,w=0,n_points=2000):
        #time_step=self.custFunc.custom_times[1]/1000
        time_step=self.custFunc.InterpStep
        #print start_time,endTime
        npoints=int(endTime/time_step)
        time=np.linspace(0.0,endTime,npoints)
        vec=[]

        for t in time:
            vec.append(self.custFunc.getValue(w, t))
        #vec_interp=interpolate.splrep(vec,time,s=0)
        
        if self.movementType==1:
            self.DisplacementCustom=interpolate.splrep(time,vec,s=0)
            #print np.size(self.derivative(vec,time[1]-time[0])),self.derivative(vec,time[1]-time[0])
            self.VelocityCustom=interpolate.splrep(time,self.derivative(vec,time[1]-time[0]),s=0)
        elif self.movementType==2:
            self.DisplacementCustom=interpolate.splrep(time,self.integrate(vec,time),s=0)
            self.VelocityCustom=interpolate.splrep(time,vec,s=0)
        else:
            int_vec=self.integrate(vec,time)
            self.VelocityCustom=interpolate.splrep(time,int_vec,s=0)
            self.DisplacementCustom=interpolate.splrep(time,self.integrate(int_vec,time),s=0)
        
    
    def integrate(self,vector,time):
        result=[]
        for i in range(0,len(time)):
            result.append(trapz(vector[0:i],time[0:i]))
        return result
    
    def derivative(self,vector,h):
        """
        Calculating by using central differnce derivative, while first and last values
        are calculated by forward and backward differences
        """
        result=[]
        result.append((vector[1]-vector[0])/h)
        for i in range(1,len(vector)-1):
            result.append((vector[i+1]-vector[i-1])/2/h)
        result.append((vector[-1]-vector[-2])/h)
        return result
    
    def getFunction(self,w,t):
        if self.custFunc.type==1:
            S=sin(w*t)
            C=cos(w*t)
            if self.movementType==1:
                Displacement=S*self.custFunc.A+C*self.custFunc.B
                Velocity=C/w*self.custFunc.A-S/w*self.custFunc.B
            elif self.movementType==2:
                Displacement=-C/w*self.custFunc.A+S/w*self.custFunc.B
                Velocity=S*self.custFunc.A+C*self.custFunc.B
            else:
                w_sq=w**2
                Displacement=-S/w_sq*self.custFunc.A-C/w_sq*self.custFunc.B
                Velocity=-C/w*self.custFunc.A+S/w*self.custFunc.B
#                Vector=[[-cos(w*t)/w,sin(w*t)/w],[sin(w*t),cos(w*t)]]
#                VelVector=[[-cos(w*t)/w,sin(w*t)/w],[sin(w*t),cos(w*t)]]
#                AccelVector=[[-sin(w*t)/(w**2),-cos(w*t)/(w**2)],[-cos(w*t)/w,sin(w*t)/w]]
#                Vector={1:DispVector,2:VelVector,3:AccelVector}[self.movementType]
#                Displacement=Vector[0][0]*self.custFunc.A+Vector[0][1]*self.custFunc.B
#                Velocity=Vector[1][0]*self.custFunc.A+Vector[1][1]*self.custFunc.B
        else:
            Displacement=interpolate.splev(t,self.DisplacementCustom)
            Velocity=interpolate.splev(t,self.VelocityCustom)
            #print t,Displacement
        return Displacement,Velocity
       
        

    def configure(self,available_nodes,nodeIndex=1):
        DispDialog=DisplacementDlg(nodeIndex,self.custFunc, available_nodes,self.funcType,self.movementType)
        if DispDialog.exec_():
            self.node,self.funcType,self.movementType,self.custFunc=DispDialog.retrieve_data()
            return 1
        return 0
        
class Force:
    def __init__(self,node=1):
        self.supported={1:'Function'}
        self.custFunc=CustomFunc()
        self.node=node

    
    def getValue(self,w,t):
        return self.custFunc.getValue(w, t)
    
    def configure(self,available_nodes,nodeIndex=1):
        ForceDialog=ForceDlg(available_nodes,nodeIndex,self.custFunc)
        if ForceDialog.exec_():
            self.node,self.custFunc=ForceDialog.retrieve_data()
            return 1
        return 0


class ForceDlg(QDialog, ForceDialog.Ui_ForceDialog):
    def __init__(self,available_nodes, nodeIndex,custFunc,parent=None):
        super(ForceDlg,self).__init__(parent)
        self.setupUi(self)
        for i in available_nodes:
            self.comboBoxNode.addItem(str(i+1))
        self.comboBoxNode.setCurrentIndex(nodeIndex-1)
        self.custFunc=custFunc
        
    @pyqtSignature("")
    def on_EditButton_clicked(self):
        self.custFunc.configure()
        
    def retrieve_data(self):
        node=self.comboBoxNode.currentIndex()
        return node, self.custFunc
      
class DisplacementDlg(QDialog, DisplacementDialog.Ui_Dialog):
    def __init__(self,nodeIndex,custFunc,available_nodes,funcType=1,movementType=1,parent=None):
        super(DisplacementDlg,self).__init__(parent)
        self.setupUi(self)
        self.movementType=movementType
        self.funcType=funcType
        for i in available_nodes:
            self.comboBoxNode.addItem(str(i+1))
        self.comboBoxNode.setCurrentIndex(nodeIndex-1)
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
    form=MainWindow()
    form.show()
    app.exec_()
    