from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QTransform
from models import Note

class MarchArrowLabel(QLabel):
	
	def __init__(self, orientation, parent):
		super().__init__(parent)
		pixmap = QPixmap('../res/notes.png')
		rect = QRect(0, 0, 64, 64)

		img = pixmap.copy(rect)
		rotation = QTransform()

		if (orientation == Note.POSITION_LEFT):
			rotation.rotate(315, Qt.ZAxis)
		elif (orientation == Note.POSITION_DOWN):
			rotation.rotate(225, Qt.ZAxis)
		elif ( orientation == Note.POSITION_UP):
			rotation.rotate(45, Qt.ZAxis)
		elif (orientation == Note.POSITION_RIGHT):
			rotation.rotate(135, Qt.ZAxis)

		img = img.transformed(rotation)
		self.setPixmap(img)
		self.parent = parent

