import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QGridLayout, QGroupBox
from PyQt5.QtGui import QIcon
 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
 
import random
from params import params
from glob import glob
import os
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 1920
        self.height = 1020
        
        #self.figure = Figure()
        #self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, self)

        #self.button = QtGui.QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        data = [random.random() for i in range(10)]

        # create an axis
        #ax = self.figure.add_subplot(111)

        # discards the old graph
        #ax.clear()

        # plot data
        #ax.plot(data, '*-')
        
        #self.canvas.draw()
        
        params.wav_file_list = glob(os.path.join(params.data_dir, '*.wav')) 
        print(params.wav_file_list)
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #m = PlotCanvas(self, width=5, height=4)
        #m.move(0,0)
 
        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This s an example button')
        #button.move(500,0)
        #button.resize(140,100)

        self.layout = QGridLayout()
        
        self.createGridLayout()
        
        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
         
        #layout.addWidget(self.canvas,0,0)
        layout.addWidget(QPushButton('2'),0,1)
        layout.addWidget(QPushButton('3'),0,2)
        layout.addWidget(QPushButton('4'),1,0)
        layout.addWidget(QPushButton('5'),1,1)
        layout.addWidget(QPushButton('6'),1,2)
        layout.addWidget(QPushButton('7'),2,0)
        layout.addWidget(QPushButton('8'),2,1)
        layout.addWidget(QPushButton('9'),2,2)
         
        self.horizontalGroupBox.setLayout(layout)

 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())