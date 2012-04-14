"""
This demo demonstrates how to embed a matplotlib (mpl) plot 
into a PyQt4 GUI application, including:

* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu

The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import interpolate
import csv

#import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


class ResultExplorer(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Results Explorer')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.result_x,self.result_y=[],[]
        self.tracking_mode=False
        self.label_x,self.label_y,self.result_name=[],[],[]
        self.relative_to.addItem("Absolute")

        #self.textbox.setText('1 2 3 4')
        #self.on_draw()
        
    def set_default_result(self,index):
        self.choose_result.setCurrentIndex(index)
        self.add_clicked()
        
    def add_result(self,name,x,y,label_x,label_y):
        self.result_name.append(name)
        self.result_x.append(x)
        self.result_y.append(y)
        self.label_x.append(label_x)
        self.label_y.append(label_y)
        self.update_available_results()
        
    
    def add_custom_text(self,text):
        self.textedit.append(text)
        
    def update_available_results(self):
        self.choose_result.clear()
        self.relative_to.clear()
        self.relative_to.addItem("Absolute") 
        for i in self.result_name:
            self.choose_result.addItem(i)
            self.relative_to.addItem(i)
    
    
        
    def clear(self):
        self.result_x,self.result_y=[],[]
        self.label_x,self.label_y,self.result_name=[],[],[]
        self.clear_clicked()
        self.textedit.clear()
    
    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
    
    def save_csv_plot(self):
        file_choices = "csv(*.csv)|*.csv"
        path = unicode(QFileDialog.getSaveFileName(self, 'Save file', '', file_choices))
        if path:
            print path
            caption_row=[]
            csvWriter = csv.writer(open(path, 'wb'), delimiter=' ',  quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(self.result_name)
            for i in range(0,len(self.result_name)):
                caption_row=caption_row+[self.label_x[i]]+[self.label_y[i]]
            csvWriter.writerow(caption_row)
            #print len(self.result_x[0]),len(self.result_name)
            for j in range (0,len(self.result_x[0])):
                row=[]
                for i in range(0,len(self.result_name)):
                    row=row+[self.result_x[i][j]]+[self.result_y[i][j]]
                csvWriter.writerow(row)
                

        
    
    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:
        
         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        QMessageBox.about(self, "About the demo", msg.strip())
    

    
    
    def add_clicked(self):
        self.tracking_clicked(default='False')
        relativeResult=0
        current=self.choose_result.currentIndex()
        relativeTo=self.relative_to.currentIndex()
        if relativeTo:
            relativeResult=self.result_y[relativeTo-1]
        self.interpolated_result=interpolate.splrep(self.result_x[current],np.array(self.result_y[current])-np.array(relativeResult),s=0)
        self.axes.plot(self.result_x[current],np.array(self.result_y[current])-np.array(relativeResult),picker=1)
        self.txt = self.axes.text( 0.7, 0.9, '', transform=self.axes.transAxes)
        self.axes.set_xlabel(self.label_x[current],fontsize=9)
        self.axes.set_ylabel(self.label_y[current],fontsize=9)
        self.axes.grid(True)
        self.format_labels()
        self.canvas.draw()
        #self.on_draw()
        
    def replace_clicked(self):
        self.clear_clicked()
        self.add_clicked()
    
    def intersect_clicked(self):
        #print "intersect clicked"
        try:
            x=self.intersect_textbox.text().toFloat()[0]
            y=interpolate.splev(x,self.interpolated_result)
            self.add_custom_text("Query result: x = "+str(x)+', y = '+str(y))
            self.axes.plot([x],[y], marker='+', color='r', ls='')
            self.canvas.draw()
        except:
            QMessageBox.information(self,"Error!", "Probably add the plot first")
        
        
        
       
        
        
    def format_labels(self):
        labels_x = self.axes.get_xticklabels()
        labels_y = self.axes.get_yticklabels()
        for xlabel in labels_x:
                xlabel.set_fontsize(9)
        for ylabel in labels_y:
                ylabel.set_fontsize(9)
                #ylabel.set_color('b')
    
    def clear_clicked(self):
        self.axes.clear()
        del self.tracking_dot
        self.canvas.draw()
    
    def tracking_clicked(self,default='Switch'):
        
        if default=='Switch':
            self.tracking_mode=not self.tracking_mode
        else: 
            self.tracking_mode=False
        self.add_custom_text("Tracking mode: "+str(self.tracking_mode))
        if hasattr(self, 'tracking_dot'):
            l=self.tracking_dot.pop()
            l.remove()
            del self.tracking_dot
         
               # print "Some error has occured"
        self.canvas.draw()
    
    def on_draw(self):
        """ Redraws the figure
        """
#        str = unicode(self.textbox.text())
#        self.data = map(int, str.split())
#        
#        x = range(len(self.data))
#
#        # clear the axes and redraw the plot anew
#        #
#        self.axes.clear()        
#        self.axes.grid(self.grid_cb.isChecked())
#        
#        self.axes.bar(
#            left=x, 
#            height=self.data, 
#            width=self.slider.value() / 100.0, 
#            align='center', 
#            alpha=0.44,
#            picker=5)

    
    def mouse_move(self,event):
       
        if not (event.inaxes and self.tracking_mode and hasattr(self, 'interpolated_result')) : return
        x, y = event.xdata, event.ydata
        y=interpolate.splev(x,self.interpolated_result) 
        self.txt.set_text( 'x=%1.5f, y=%1.5f'%(x,y) )
        if hasattr(self, 'tracking_dot'):
            try:
                l=self.tracking_dot.pop()
                l.remove()
            except:
                pass
        self.tracking_dot=self.axes.plot([x],[y], marker='o', color='r', ls='')
        self.canvas.draw()
        
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
         # Create the navigation toolbar, tied to the canvas
        #

        self.fig = Figure((10.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95)

        
        # Bind the 'pick' event for clicking on one of the bars
        #
        #self.canvas.mpl_connect('pick_event', self.on_pick)
        
       
        
        # Other GUI controls
        # 
        self.choose_result = QComboBox()
        self.label1=QLabel("Active Result:")
        self.label2=QLabel("Relative to:")
        self.relative_to=QComboBox()
        self.label3=QLabel("Query X: ")
        self.intersect_textbox=QLineEdit()
        self.intersect_button=QPushButton("&Find intersect.")
        self.tracking_button=QPushButton("Tracking mode")
        self.intersect_textbox.setMaximumWidth(75)
        #self.connect(self.choose_result, SIGNAL('currentIndexChanged (int)'), self.on_draw)
        
        self.add_button = QPushButton("&Add Plot")
        self.clear_button = QPushButton("&Clear Plots")
        self.textedit=QTextEdit()
        self.replace_button=QPushButton("&Replace Plot")
   
        self.connect(self.add_button, SIGNAL('clicked()'), self.add_clicked)
        self.connect(self.clear_button, SIGNAL('clicked()'), self.clear_clicked)
        self.connect(self.replace_button, SIGNAL('clicked()'), self.replace_clicked)
        self.connect(self.intersect_button, SIGNAL('clicked()'), self.intersect_clicked)
        self.connect(self.tracking_button, SIGNAL('clicked()'), self.tracking_clicked)
        self.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        

        hbox = QHBoxLayout()
#        

        hbox.addWidget(self.label1)
        hbox.addWidget(self.choose_result)
        hbox.addWidget(self.label2)
        hbox.addWidget(self.relative_to)
        hbox.addStretch()
        hbox.addWidget(self.tracking_button)
        hbox.addStretch()
        hbox.addWidget(self.label3)
        hbox.addWidget(self.intersect_textbox)
        hbox.addWidget(self.intersect_button)
        hbox1=QHBoxLayout()
        hbox1.addWidget(self.add_button)
        hbox1.addWidget(self.replace_button)
        hbox1.addWidget(self.clear_button)
        hbox1.addStretch()
        vbox1=QVBoxLayout()
        vbox1.addLayout(hbox)
        vbox1.addLayout(hbox1)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)


        vbox.addLayout(vbox1)
        vbox.addStretch()
        vbox.addWidget(self.textedit)
        vbox.addStretch()
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
    def create_status_bar(self):
        self.status_text = QLabel("Ready.")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")
        export_csv_action = self.create_action("&Export to .CSV",
            shortcut="Ctrl+E", slot=self.save_csv_plot, 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, export_csv_action,None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    t=np.linspace(0,np.pi*2,100)
    app = QApplication(sys.argv)
    form = ResultExplorer()
    form.add_result("Sinus", t, np.sin(t), "Time [sec]", "Disp")
    form.add_result("Cosine", t, np.cos(t), "Time [sec]", "Disp")
    
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
