from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
from PyQt5 import QtCore, QtWidgets, QtGui

import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from glob import glob
import librosa
import threading
from scipy.io import wavfile

from playsound import playsound

from params import params

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		pass


class MyStaticMplCanvas(MyMplCanvas):
	"""Simple canvas with a sine plot."""

	def compute_initial_figure(self):
		t = arange(0.0, 3.0, 0.01)
		s = sin(2*pi*t)
		self.axes.plot(t, s)

class WavCanvas(FigureCanvas):
	def __init__(self, data_path, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.load_wav(data_path)
		self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)

		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		t = arange(0, len(self.data)/self.fs, 1/self.fs)
		self.axes.plot(t, self.data)
		self.axes.axis('off')

	def redraw_figure(self, color):
		t = arange(0, len(self.data)/self.fs, 1/self.fs)
		self.axes.plot(t, self.data, color)
		self.axes.axis('off')
		self.draw()

	def mousePressEvent(self, event):
		self.redraw_figure('tab:red')
		sound_thread = threading.Thread(target=self.play_wav)
		sound_thread.start()

		# self.redraw_figure('b')

	def load_wav(self, data_path):
		self.data_path = data_path
		self.fs, y = wavfile.read(self.data_path)
		self.data = y[:, 0]

	def play_wav(self):
		playsound(self.data_path)
		self.redraw_figure('tab:blue')



class MyDynamicMplCanvas(MyMplCanvas):
	"""A canvas that updates itself every second with a new plot."""

	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.update_figure)
		timer.start(1000)

	def compute_initial_figure(self):
		self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

	def update_figure(self):
		# Build a list of 4 random integers between 0 and 10 (both inclusive)
		l = [random.randint(0, 10) for i in range(4)]
		self.axes.cla()
		self.axes.plot([0, 1, 2, 3], l, 'r')
		self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setWindowTitle("application main window")

		self.file_menu = QtWidgets.QMenu('&File', self)
		self.file_menu.addAction('&Quit', self.fileQuit,
								 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		self.help_menu = QtWidgets.QMenu('&Help', self)
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)

		self.help_menu.addAction('&About', self.about)

		self.main_widget = QtWidgets.QWidget(self)

		self.wav_file_list = glob(os.path.join(params.data_dir, '*.wav')) 
		print(self.wav_file_list)

		self.wav_data_list = list()

		for i, wav_file_path in enumerate(self.wav_file_list):
			print(wav_file_path)
			#y = librosa.core.load(wav_file_path, sr=None, dtype=np.float32)
			fs, y = wavfile.read(wav_file_path)
			y = y[:, 0]
			self.wav_data_list.append(y)
			self.fs = fs

		# l = QtWidgets.QVBoxLayout(self.main_widget)
		l = QtWidgets.QGridLayout(self.main_widget)
		
		l.setColumnStretch(0, 1)
		l.setColumnStretch(1, 3)
		l.setColumnStretch(2, 3)
		l.setColumnStretch(3, 3)
		l.setColumnStretch(4, 3)
		l.setColumnStretch(5, 1)

		l.setRowStretch(0, 1)
		l.setRowStretch(1, 3)
		l.setRowStretch(2, 3)
		l.setRowStretch(3, 3)
		l.setRowStretch(4, 3)
		l.setRowStretch(5, 1)

		self.plot_list = list()
		for i in range(16):
			self.plot_list.append(WavCanvas(self.wav_file_list[i], self.main_widget, width=5, height=4, dpi=100))
			# self.plot_list.append(MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100))

		# sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		# dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		# dc2 = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		
		for i in range(1, 5):
			for j in range(1, 5):			
				l.addWidget(self.plot_list[4*(i-1)+j-1], i, j)

		# l.addWidget(sc, 1, 1)
		# l.addWidget(dc2, 2, 1)
		# l.addWidget(dc, 3, 1)

		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)

		self.statusBar().showMessage("All hail matplotlib!", 2000)

	def fileQuit(self):
		self.close()

	def closeEvent(self, ce):
		self.fileQuit()

	def about(self):
		QtWidgets.QMessageBox.about(self, "About",
									"""embedding_in_qt5.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen

This program is a simple example of a Qt5 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation.

This is modified from the embedding in qt4 example to show the difference
between qt4 and qt5"""
								)


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()