from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout

class MarchNavigationView(QWidget):
	def __init__(self, parent):
		super(MarchNavigationView, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.layout = QVBoxLayout()
		
