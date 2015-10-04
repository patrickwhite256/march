from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout, QPushButton, QSlider
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QRect
from models import Chart, Note
from .arrow_label import MarchArrowLabel

INTERVAL_SPACING = 100

class MarchTrackView(QWidget):
	def __init__(self, parent, model):
		super().__init__(parent)
		
		# Properties
		self.interval = 4

		self.setModel(model)
		self.initUI()

	def initUI(self):
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		scale = QSlider(Qt.Vertical, self)
		scale.valueChanged.connect(self.intervalChangeEvent)
		scale.setMinimum(4)
		scale.setMaximum(192)
		scale.setTickInterval(4)

		leftArrow = MarchArrowLabel(Note.POSITION_LEFT, self)
		downArrow = MarchArrowLabel(Note.POSITION_DOWN, self)
		upArrow = MarchArrowLabel (Note.POSITION_UP, self)
		rightArrow = MarchArrowLabel(Note.POSITION_RIGHT, self)

		self.layout = QVBoxLayout()
		self.layout.addWidget(leftArrow)
		self.layout.addWidget(downArrow)
		self.layout.addWidget(upArrow)
		self.layout.addWidget(rightArrow)
		self.layout.addWidget(scale)

		self.setLayout(self.layout)
		self.updateGeometry()

	def setModel(self, chart):
		'''
		Set the model of the track. 
		The model should be a Chart object.
		'''
		self.model = chart

	def drawChart(self, qp):

		brush = QBrush(Qt.red, Qt.SolidPattern)
		qp.setBrush(brush)
	#	qp.drawRect(self.rect())

		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		
		y = 0	
		for measure in self.model.measures:
			qp.drawLine(100, y, 400, y)
			y += self.interval * 10 



	# Event Handlers

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawChart(qp)
		qp.end()

	def intervalChangeEvent(self, data):
		self.interval = data
		self.update()

