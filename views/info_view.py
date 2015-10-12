from PyQt5.QtCore import QFile, QFileInfo
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout, QFormLayout, QLabel, QLineEdit


class MarchInfoView(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.initUI()

	def initUI(self):
		self.layout = QVBoxLayout()					
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.setContentsMargins(4, 4, 4, 4)  # just something smaller, imo
		self.setMaximumHeight(384)  # 768/3
		self.setMaximumWidth(256)  # 1024/4
		
		self.formLayout = QFormLayout()
		title = QLineEdit(self)
		artist = QLineEdit(self)
		chartBackground = QLineEdit(self)
		subtitle = QLineEdit(self)
		banner = QLineEdit(self)

		self.formLayout.addRow(self.tr("&Title:"), title)
		self.formLayout.addRow(self.tr("&Artist:"), artist)
		self.formLayout.addRow(self.tr("&Chart Background:"), chartBackground)
		self.formLayout.addRow(self.tr("&Subtitle:"), subtitle)
		self.formLayout.addRow(self.tr("&Banner:"), banner)
		self.setLayout(self.formLayout)

