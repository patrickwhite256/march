from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
	
class MarchNoteView(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.initUI()

	def initUI(self):
		self.layout = QVBoxLayout()
