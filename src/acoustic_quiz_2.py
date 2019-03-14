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
import random
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

num_answer = -1
player_answer = -1
['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']

class WavCanvas(FigureCanvas):
	def __init__(self, data_path, num, noise_file, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.load_wav(data_path)
		self.compute_initial_figure()
		self.noise_file = noise_file[0]
		self.num = num

		FigureCanvas.__init__(self, fig)

		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		# t = arange(0, len(self.data)/self.fs, 1/self.fs)
		# self.axes.plot(t, self.data)

		new_fs = self.fs/20
		new_data = librosa.core.resample(self.data, self.fs, new_fs)
		t = arange(0, len(new_data)/new_fs, 1/new_fs)
		self.axes.plot(t, new_data)

		self.axes.axis('off')
		# self.axes.axes.margins(tight=True)

	def redraw_figure(self, color):
		new_fs = self.fs/20
		new_data = librosa.core.resample(self.data, self.fs, new_fs)
		t = arange(0, len(new_data)/new_fs, 1/new_fs)
		self.axes.plot(t, new_data, color)
		# t = arange(0, len(self.data)/self.fs, 1/self.fs)
		# self.axes.plot(t, self.data, color)
		self.axes.axis('off')
		self.draw()

	def mousePressEvent(self, event):
		self.axes.cla()
		self.redraw_figure('tab:red')
		sound_thread = threading.Thread(target=self.play_wav)
		sound_thread.start()
		print('Playing Sound {:d}:{:d}'.format(num_answer, self.num))

		if (num_answer == self.num):
			print('Playing Noise {:d}:{:d}'.format(num_answer, self.num))
			noise_thread = threading.Thread(target=self.play_noise)
			noise_thread.start()

		# self.redraw_figure('b')

	def load_wav(self, data_path):
		self.data_path = data_path

		# self.fs, y = wavfile.read(self.data_path)
		y, self.fs = librosa.core.load(self.data_path, duration=3)
		self.data = y

	def play_wav(self):
		try:
			playsound(self.data_path)
		except:
			print("Error in play_sound thread")
		self.axes.cla()
		self.redraw_figure('tab:blue')

	def play_noise(self):
		try:
			print('Noise Playing ...')
			playsound(self.noise_file)
		except:
			print("Error in play_sound thread")

class SpectrogramCanvas(FigureCanvas):
	def __init__(self, data_path, num, noise_file, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.noise_file = noise_file[0]
		self.num = num

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
		self.axes.set_ylim(0, 2000)
		self.axes.axis('off')

	def mousePressEvent(self, event):
		sound_thread = threading.Thread(target=self.play_wav)
		sound_thread.start()
		print('Playing Sound {:d}:{:d}'.format(num_answer, self.num))

		if (num_answer == self.num):
			print('Playing Noise {:d}:{:d}'.format(num_answer, self.num))
			noise_thread = threading.Thread(target=self.play_noise)
			noise_thread.start()

		# self.redraw_figure('b')

	def load_wav(self, data_path):
		self.data_path = data_path

		# self.fs, y = wavfile.read(self.data_path)
		y, self.fs = librosa.core.load(self.data_path, duration=3)

		if self.num == num_answer:
			noise, fs = librosa.core.load(self.noise_file, duration=3)
			y = y + 5 * noise

		self.data = y

	def play_wav(self):
		try:
			playsound(self.data_path)
		except:
			print("Error in play_sound thread")

	def play_noise(self):
		try:
			print('Noise Playing ...')
			playsound(self.noise_file)
		except:
			print("Error in play_noise thread")

####

class Second(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(Second, self).__init__(parent)
		self.setFixedSize(290, 160)
		self.progress = QtWidgets.QProgressBar(self)
		self.progress.setGeometry(40, 80, 250, 20)

####

class MyButton(QtWidgets.QPushButton):
	def __init__(self, text, num, parent = None):
		super(MyButton, self).__init__()
		self.setText(text)
		self.num = num
		# print('I am button #{:d}'.format(self.num))

####
class ApplicationWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.file_menu = QtWidgets.QMenu('&File', self)
		self.file_menu.addAction('&Quit', self.fileQuit,
								 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		self.help_menu = QtWidgets.QMenu('&Help', self)
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)

		self.help_menu.addAction('&About', self.about)

		self.main_widget = QtWidgets.QWidget(self)
		self.setFixedSize(1600, 900)
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QtCore.Qt.white)
		self.setPalette(p)

		self.wav_file_list = glob(os.path.join(params.data_dir, '*.wav')) 
		
		self.normal_file = glob(os.path.join(params.data_dir, 'normal/*.wav')) 
		self.fault_file = glob(os.path.join(params.data_dir, 'fault/*.wav')) 
		self.noise_file = glob(os.path.join(params.data_dir, 'noise/*.wav')) 

		# print(self.wav_file_list)

		# self.wav_data_list = list()

		# for i, wav_file_path in enumerate(self.wav_file_list):
		# 	# print(wav_file_path)
		# 	y, fs = np.asarray(librosa.core.load(wav_file_path, duration=3))
		# 	# fs, y = wavfile.read(wav_file_path)
		# 	# print(y)
		# 	# y = y[:, 0]
		# 	self.wav_data_list.append(y)
		# 	self.fs = fs

		self.layout = QtWidgets.QGridLayout(self.main_widget)
		self.setDefaultLayout()
		self.setIntroLayout()

		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)
		self.loadDefaultLayout()

	def assignLabel(self):
		self.title_list = []
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		self.title_list = list()
		for i in range(1, 10):
			global player_answer
			# if (i == player_answer):
			# 	font.setBold(True)
			# else:
			# 	font.setBold(False)
			text = "\n{:d}".format(i)
			label = QtWidgets.QLabel(text, self)
			label.setFont(font)
			if (i == player_answer):
				label.setStyleSheet("color: rgba(255, 79, 0); font-size: 24pt; font-weight: 600;")
			label.setAlignment(Qt.Qt.AlignCenter)
			self.title_list.append(label)

	def assignButton(self):
		self.button_list = []
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		self.title_list = list()

		for i in range(1, 10):
			global player_answer
			if (i == player_answer):
				font.setBold(True)
			else:
				font.setBold(False)
			text = "{:d}".format(i)
			# button = QtWidgets.QPushButton(text, self)   
			button = MyButton(text, i, self)   
			button.setFont(font)
			# button.clicked.connect(self.print_test)
			# button.clicked.connect(self.on_click)
			button.clicked.connect(lambda state, x=i: self.buttonTest(x))
			self.button_list.append(button)

		# for i in range(0, 9):
			# self.button_list[i].clicked.connect(lambda button = self.button_list[i]: self.buttonClick(button))
			# self.button_list[i].
		# for i in range(len(self.button_list)):
		# 	self.button_list[i].clicked.connect(self.buttonClick(self.button_list[i]))

	def buttonTest(self, num):
		global player_answer
		player_answer = num
		print(player_answer)
		self.loadSpectrogramLayout()

	# def print_test(self, num):
	# 	print('Hello ~ {:d}'.format(num))

	def setLayout(self):
		self.layout.setColumnStretch(0, 1)
		self.layout.setColumnStretch(1, 3)
		self.layout.setColumnStretch(2, 1)
		self.layout.setColumnStretch(3, 3)
		self.layout.setColumnStretch(4, 1)
		self.layout.setColumnStretch(5, 3)
		self.layout.setColumnStretch(6, 1)

		self.layout.setRowStretch(0, 1)
		self.layout.setRowStretch(1, 1)
		self.layout.setRowStretch(2, 3)
		self.layout.setRowStretch(3, 1)
		self.layout.setRowStretch(4, 3)
		self.layout.setRowStretch(5, 1)
		self.layout.setRowStretch(6, 3)
		self.layout.setRowStretch(7, 1)

	def setDefaultLayout(self):
		self.layout.setColumnStretch(0, 1)
		self.layout.setColumnStretch(1, 3)
		self.layout.setColumnStretch(2, 1)
		self.layout.setColumnStretch(3, 3)
		self.layout.setColumnStretch(4, 1)

		self.layout.setRowStretch(0, 1)
		self.layout.setRowStretch(1, 1)
		self.layout.setRowStretch(2, 5)
		self.layout.setRowStretch(3, 1)

	def setQuizLayout(self):
		self.assignLabel()
		self.assignButton()
		self.setLayout()
		self.plot_list = list()

		for i in range(9):
			self.plot_list.append(WavCanvas(self.wav_file_list[i], i+1, self.noise_file, self.main_widget, width=5, height=4, dpi=100))

		for i in range(1, 4):
			for j in range(1, 4):			
				self.layout.addWidget(self.plot_list[3*(i-1)+j-1], 2*i, 2*j-1)

		for i in range(1, 4):
			for j in range(1, 4):			
				self.layout.addWidget(self.button_list[3*(i-1)+j-1], 2*i-1, 2*j-1)


		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)

		button = QtWidgets.QPushButton('<<<', self)
		button.clicked.connect(self.loadDefaultLayout)
		button.setFont(font)
		self.layout.addWidget(button, 0, 0)

		reset_button = QtWidgets.QPushButton('>>>', self)
		reset_button.clicked.connect(self.loadSpectrogramLayout)
		reset_button.setFont(font)
		self.layout.addWidget(reset_button, 0, 6)

	def loadQuizLayout(self):
		QtWidgets.QWidget().setLayout(self.layout)
		self.layout = QtWidgets.QGridLayout(self.main_widget)
		self.setWindowTitle("OnePredict Quiz Application")
		self.statusBar().showMessage("Quiz Mode", 2000)
		global num_answer 
		num_answer = random.randrange(1, 10)
		global player_answer
		player_answer = -1
		self.setQuizLayout()

	def loadSpectrogramLayout(self):
		QtWidgets.QWidget().setLayout(self.layout)
		self.layout = QtWidgets.QGridLayout(self.main_widget)
		self.setWindowTitle("OnePredict Quiz Application")
		self.statusBar().showMessage("Spectrogram Mode", 2000)
		self.setSpectrogramLayout()

	def loadDefaultLayout(self):
		QtWidgets.QWidget().setLayout(self.layout)
		self.layout = QtWidgets.QGridLayout(self.main_widget)
		self.setWindowTitle("OnePredict Quiz Application")
		self.statusBar().showMessage("Back to Introduction Page", 2000)
		self.setIntroLayout()


	def setIntroLayout(self):
		font = QtGui.QFont()
		font.setPointSize(36)
		font.setBold(True)

		normLabel = QtWidgets.QLabel("Normal", self)
		normLabel.setFont(font)
		normLabel.setAlignment(Qt.Qt.AlignCenter)

		faultLabel = QtWidgets.QLabel("Fault", self)		
		faultLabel.setFont(font)
		faultLabel.setAlignment(Qt.Qt.AlignCenter)

		normal_canvas = WavCanvas(self.normal_file[0], 0, self.noise_file, self.main_widget, width=5, height=4, dpi=100)
		fualt_canvas = WavCanvas(self.fault_file[0], 0, self.noise_file, self.main_widget, width=5, height=4, dpi=100)

		button = QtWidgets.QPushButton('>>>', self)
		button.clicked.connect(self.loadQuizLayout)
		font.setPointSize(24)
		button.setFont(font)
		self.layout.addWidget(button, 0, 4)


		self.layout.addWidget(normLabel, 1, 1)
		self.layout.addWidget(faultLabel, 1, 3)

		self.layout.addWidget(normal_canvas, 2, 1)
		self.layout.addWidget(fualt_canvas, 2, 3)


	def setSpectrogramLayout(self):
		self.assignLabel()
		self.setLayout()
		self.img_list = list()
		for i in range(9):
			self.img_list.append(SpectrogramCanvas(self.wav_file_list[i], i+1, self.noise_file, self.main_widget, width=5, height=4, dpi=100))

		for i in range(1, 4): 
			for j in range(1, 4):			
				self.layout.addWidget(self.img_list[3*(i-1)+j-1], 2*i, 2*j-1)

		for i in range(1, 4):
			for j in range(1, 4):			
				self.layout.addWidget(self.title_list[3*(i-1)+j-1], 2*i-1, 2*j-1)

		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)

		button = QtWidgets.QPushButton('<<<', self)
		button.setFont(font)
		button.clicked.connect(self.loadQuizLayout)
		self.layout.addWidget(button, 0, 0)

		button = QtWidgets.QPushButton('>>>', self)
		button.setFont(font)
		button.clicked.connect(self.loadDefaultLayout)
		self.layout.addWidget(button, 0, 6)



	def on_click(self):
		self.close()

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
			self.loadSpectrogramLayout()
			
		if event.key() == QtCore.Qt.Key_P:
			self.loadQuizLayout()

		if event.key() == QtCore.Qt.Key_O:
			QtWidgets.QWidget().setLayout(self.layout)
			self.layout = QtWidgets.QGridLayout(self.main_widget)
			self.dialog = Second(self)
			self.dialog.show()
	

qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()