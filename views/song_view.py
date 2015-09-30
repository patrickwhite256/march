from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
		
class MarchSongSelectView(QWidget):
	def __init__(self, parent):
		super(MarchSongSelectView, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.layout = QVBoxLayout()
