from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QTransform, QPainter, QBrush
from models import Note, Hold

class MarchArrowLabel(QLabel):
	
	def __init__(self, orientation, parent):
		super().__init__(parent)
		self.orientation = orientation
		self.initUI()

	def initUI(self):
		pixmap = QPixmap('res/notes.png')

		if(pixmap.isNull()):
			print("Sorry, there's something wrong with the image file")

		rect = QRect(0, 0, 64, 64)

		img = pixmap.copy(rect)
		if(img.isNull()):
			print("Something went wrong when cropping")
	
		rotation = QTransform()

		if (self.orientation == Note.POSITION_LEFT):
			rotation.rotate(315, Qt.ZAxis)
		elif (self.orientation == Note.POSITION_DOWN):
			rotation.rotate(225, Qt.ZAxis)
		elif ( self.orientation == Note.POSITION_UP):
			rotation.rotate(45, Qt.ZAxis)
		elif (self.orientation == Note.POSITION_RIGHT):
			rotation.rotate(135, Qt.ZAxis)

		img = img.transformed(rotation)
		
		self.setPixmap(img)
	#	self.setGeometry(0, 0, 64, 64)
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

class MarchBombLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        pixmap = QPixmap('res/bombs.png')
        rect = QRect(0, 0, 64, 64)
        img = pixmap.copy(rect)
        self.setPixmap(img)

class MarchHoldLabel(QLabel):
    def __init__(self, hold_type, parent):
        super().__init__(parent)
        self.hold_type = hold_type
        self.initUI()

    def initUI(self):
        pixmap = QPixmap()
        if (self.hold_type == Hold.TYPE_HOLD):
            pixmap.load('res/hold.png')
        elif (self.hold_type == Hold.TYPE_ROLL):
            pixmap.load('res/roll.png')

        self.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))

