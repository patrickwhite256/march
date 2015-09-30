from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout

class MarchTrackView(QWidget):
	def __init__(self, parent):
		super(MarchTrackView, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.layout = QVBoxLayout()
