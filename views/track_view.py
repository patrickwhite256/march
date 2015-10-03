from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from models import Chart


INTERVAL_SPACING = 100

class MarchTrackView(QWidget):
	def __init__(self, parent, model):
		super(MarchTrackView, self).__init__(parent)
		
		# Properties
		self.interval = 4

		self.setModel(model)
		self.initUI()

	def initUI(self):
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.drawChart()
		
		self.layout = QVBoxLayout()

	def setModel(self, chart):
		'''
		Set the model of the track. 
		The model should be a Chart object.
		'''
		self.model = chart

	def drawChart(self):
		qp = QPainter()
		qp.begin(self)
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		
		y = 0	
		for measure in self.model.measures:
			qp.drawLine(100, y, 400, y)
			y += self.interval * INTERVAL_SPACING

		qp.end()

	def paintEvent(self, e):
		self.drawChart()
