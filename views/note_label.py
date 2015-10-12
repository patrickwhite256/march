from PyQt5.QtWidgets import QLabel
from models import Tap, Hold

class MarchNoteLabel(QLabel):

	def __init__(self, note_type, parent):
		super().__init__(parent)
		self.note_type = note_type
		self.initUI()

	def initUI(self):
		if (self.note_type == Tap.TYPE_NORMAL):
			self.setText('Normal Arrow')
		elif (self.note_type == Tap.TYPE_MINE):
			self.setText('Mine')
		elif (self.note_type == Hold.TYPE_HOLD):
			self.setText('Hold Note')
		elif (self.note_type == Hold.TYPE_ROLL):
			self.setText('Roll Note')
	
