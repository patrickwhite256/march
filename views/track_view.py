from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout, QPushButton, QSlider
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QRect
from models import Chart, Note
from .arrow_label import MarchArrowLabel

INTERVAL_SPACING = 10
ARROW_SPACING = 80

class MarchTrackView(QWidget):

	column = -1
	row = -1

	def __init__(self, parent, model):
		super().__init__(parent)
		
		# Properties
		self.interval = 4

		self.setModel(model)
		self.initUI()
		self.setMouseTracking(True)

	def initUI(self):
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		scale = QSlider(Qt.Vertical, self)
		scale.valueChanged.connect(self.intervalChangeEvent)
		scale.setMinimum(4)
		scale.setMaximum(192)
		scale.setTickInterval(4)

		leftArrow = MarchArrowLabel(Note.POSITION_LEFT, self)
		leftArrow.move(90, 50)
		leftArrow.show()
		downArrow = MarchArrowLabel(Note.POSITION_DOWN, self)
		downArrow.move(90 + ARROW_SPACING, 50)
		downArrow.show()
		upArrow = MarchArrowLabel (Note.POSITION_UP, self)
		upArrow.move(90 + ARROW_SPACING * 2, 50)
		upArrow.show()
		rightArrow = MarchArrowLabel(Note.POSITION_RIGHT, self)
		rightArrow.move(90 + ARROW_SPACING * 3, 50)
		rightArrow.show()

		self.layout = QVBoxLayout()
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

		for i, measure in enumerate(self.model.measures):
			if (i == self.row):
				qp.setPen(QPen(Qt.red, 4, Qt.SolidLine))
			else:
				qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))	
			
			y = i * self.interval * INTERVAL_SPACING
			qp.drawLine(100, y, 400, y)
			
		
		if(self.column > -1):
			columnStart = 100 + ARROW_SPACING * self.column
			columnEnd = 100 + ARROW_SPACING * (self.column + 1)

			qp.drawLine(columnStart, 0, columnStart, self.height())
			qp.drawLine(columnEnd, 0, columnEnd, self.height())


	# Event Handlers

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawChart(qp)
		qp.end()

	def intervalChangeEvent(self, data):
		self.interval = data
		self.update()

	def mouseMoveEvent(self, event):
		x = event.pos().x()
		y = event.pos().y()

		self.column = min(int((x - 100) / ARROW_SPACING), 3)
		self.row = int((y + INTERVAL_SPACING / 2) / (self.interval * INTERVAL_SPACING))

		self.update()
		
				



