from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
import matplotlib.pyplot as plt
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# matplotlib.use('Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

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
		# self.axes.axes.margins(tight=True)

	def redraw_figure(self, color):
		t = arange(0, len(self.data)/self.fs, 1/self.fs)
		self.axes.plot(t, self.data, color)
		self.axes.axis('off')
		self.draw()

	def mousePressEvent(self, event):
		self.axes.cla()
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
		self.axes.cla()
		self.redraw_figure('tab:blue')

class SpectrogramCanvas(FigureCanvas):
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
		nsc = int(self.fs / 10)
		nov = int(nsc/2)

		self.axes.specgram(self.data, NFFT=nsc, Fs=self.fs,
					 noverlap=nov, mode='psd', scale='dB')
		self.axes.axis('off')

	def mousePressEvent(self, event):
		sound_thread = threading.Thread(target=self.play_wav)
		sound_thread.start()

		# self.redraw_figure('b')

	def load_wav(self, data_path):
		self.data_path = data_path
		self.fs, y = wavfile.read(self.data_path)
		self.data = y[:, 0]
		self.data = self.data.astype(float)

	def play_wav(self):
		playsound(self.data_path)

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
		# print(self.wav_file_list)

		self.wav_data_list = list()

		for i, wav_file_path in enumerate(self.wav_file_list):
			# print(wav_file_path)
			#y = librosa.core.load(wav_file_path, sr=None, dtype=np.float32)
			fs, y = wavfile.read(wav_file_path)
			y = y[:, 0]
			self.wav_data_list.append(y)
			self.fs = fs
  
		self.layout = QtWidgets.QGridLayout(self.main_widget)
		
		self.layout.setColumnStretch(0, 1)
		self.layout.setColumnStretch(1, 3)
		self.layout.setColumnStretch(2, 1)
		self.layout.setColumnStretch(3, 3)
		self.layout.setColumnStretch(4, 1)
		self.layout.setColumnStretch(5, 3)
		self.layout.setColumnStretch(6, 1)
		self.layout.setColumnStretch(7, 3)
		self.layout.setColumnStretch(8, 1)

		self.layout.setRowStretch(0, 1)
		self.layout.setRowStretch(1, 1)
		self.layout.setRowStretch(2, 3)
		self.layout.setRowStretch(3, 1)
		self.layout.setRowStretch(4, 3)
		self.layout.setRowStretch(5, 1)
		self.layout.setRowStretch(6, 3)
		self.layout.setRowStretch(7, 1)
		self.layout.setRowStretch(8, 3)
		self.layout.setRowStretch(9, 1)

		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		self.title_list = list()
		for i in range(1, 17):
			text = "\n{:d}".format(i)
			label = QtWidgets.QLabel(text, self)
			label.setFont(font)
			label.setAlignment(Qt.Qt.AlignCenter)
			self.title_list.append(label)

		for i in range(1, 5):
			for j in range(1, 5):			
				self.layout.addWidget(self.title_list[4*(i-1)+j-1], 2*i-1, 2*j-1)

		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)

	def fileQuit(self):
		self.close()

	def closeEvent(self, ce):
		self.fileQuit()

	def about(self):
		QtWidgets.QMessageBox.about(self, "About", "No message")

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

		if event.key() == QtCore.Qt.Key_Space:
			self.statusBar().showMessage("Spectrogram Mode", 2000)

			self.plot_list = list()
			for i in range(16):
				self.plot_list.append(WavCanvas(self.wav_file_list[i], self.main_widget, width=5, height=4, dpi=100))

			for i in range(1, 5):
				for j in range(1, 5):			
					self.layout.addWidget(self.plot_list[4*(i-1)+j-1], 2*i, 2*j-1)


		if event.key() == QtCore.Qt.Key_P:

			self.img_list = list()
			for i in range(16):
				self.img_list.append(SpectrogramCanvas(self.wav_file_list[i], self.main_widget, width=5, height=4, dpi=100))

			for i in range(1, 5):
				for j in range(1, 5):			
					self.layout.addWidget(self.img_list[4*(i-1)+j-1], 2*i, 2*j-1)


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()