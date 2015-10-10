from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QTransform, QPainter, QBrush
from models import Note

ARROW_SIZE = 64

class MarchArrowLabel(QLabel):
	
	def __init__(self, orientation, parent):
		super().__init__(parent)
		self.orientation = orientation
		self.initUI()

	def initUI(self):
		pixmap = QPixmap('res/basic-note.png')

		if(pixmap.isNull()):
			print("Sorry, there's something wrong with the image file")

		rect = QRect(0, 0, ARROW_SIZE, ARROW_SIZE)

		img = pixmap.copy(rect)
		if(img.isNull()):
			print("Something went wrong when cropping")
	
		rotation = QTransform()

		if (self.orientation == Note.POSITION_LEFT):
			rotation.rotate(360, Qt.ZAxis)
		elif (self.orientation == Note.POSITION_DOWN):
			rotation.rotate(270, Qt.ZAxis)
		elif (self.orientation == Note.POSITION_UP):
			rotation.rotate(90, Qt.ZAxis)
		elif (self.orientation == Note.POSITION_RIGHT):
			rotation.rotate(180, Qt.ZAxis)

		img = img.transformed(rotation)
		
		self.setPixmap(img)
	#	self.setGeometry(0, 0, ARROW_SIZE, ARROW_SIZE)
	'''	
	def paintEvent(self, e):
		super(QLabel, self).paintEvent(e)
		qp = QPainter()
		qp.begin(self)
		brush = QBrush(Qt.red, Qt.SolidPattern)
		qp.setBrush(brush)
		qp.drawRect(self.rect())
		qp.end()
	'''
