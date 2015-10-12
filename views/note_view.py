from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from .note_label import MarchNoteLabel
from models import Tap, Hold
	
class MarchNoteView(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.initUI()

	def initUI(self):
		self.layout = QVBoxLayout()
		self.normal_label = MarchNoteLabel(Tap.TYPE_NORMAL, self)
		self.mine_label = MarchNoteLabel(Tap.TYPE_MINE, self)
		self.hold_label = MarchNoteLabel(Hold.TYPE_HOLD, self)
		self.roll_label = MarchNoteLabel(Hold.TYPE_ROLL, self)

		self.layout.addWidget(self.normal_label)
		self.layout.addWidget(self.mine_label)
		self.layout.addWidget(self.hold_label)
		self.layout.addWidget(self.roll_label)
