import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

 
class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1020
        
        self.figure = Figure()
        self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        
        data = [random.random() for i in range(10)]
        ax = self.figure.add_subplot(111, figsize=(15,15))
        ax.clear()
        ax.plot(data, '*-')
        self.canvas.draw()
        
        self.initUI()
        
        
         
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
         
        self.createGridLayout()
         
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
         
        self.show()
 
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 3)
        layout.setColumnStretch(5, 1)

         
        for i in range(1, 5):
            for j in range(1, 5):
                
                if j == 1:
                    plotObject = self.canvas
                    plotObject.resize(200, 100)
                    layout.addWidget(plotObject,i,j)
                
                else: layout.addWidget(QPushButton('{:d}'.format(4*(j-1)+i)),i,j)

         
        self.horizontalGroupBox.setLayout(layout)
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())