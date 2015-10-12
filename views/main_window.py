from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from .info_view import MarchInfoView
from .song_view import MarchSongSelectView
from .nav_view import MarchNavigationView
from .track_view import MarchTrackView
from .note_view import MarchNoteView
import parse
import models

class MarchSideBarView(QFrame):
	def __init__(self, parent):
		super().__init__(parent)
		self.initUI()
	
	def initUI(self):
		self.setFrameStyle(QFrame.Box)
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.layout = QVBoxLayout()

		self.setLayout(self.layout)

	def addView(self, view):
		self.layout.addWidget(view)


# Main Window
class MarchWindow(QWidget):
	
	def __init__(self, songFile):
		super().__init__()

		self.model = models.Song()
		if(songFile is not None):
			self.model = parse.parse_song(songFile)

		self.model = models.Song()
		if(songFile is not None):
			self.model = parse.parse_song(songFile)

		self.initUI()

	
	def initUI(self):
		layout = QGridLayout()
		leftSideBar = MarchSideBarView(self)
		infoView = MarchInfoView(leftSideBar)
		songView = MarchSongSelectView(leftSideBar)
		navView = MarchNavigationView(leftSideBar)

		leftSideBar.addView(infoView)
		leftSideBar.addView(navView)
		leftSideBar.addView(songView)

		trackView = MarchTrackView(self, self.model.charts[0])

		rightSideBar = MarchSideBarView(self)
		noteView = MarchNoteView(rightSideBar)

		rightSideBar.addView(noteView)

		layout.addWidget(leftSideBar, 0, 0)
		layout.addWidget(trackView, 0, 1, 1, 2)
		layout.addWidget(rightSideBar, 0, 4)

		trackView.show()
		trackView.update()
		self.update()

		self.setWindowTitle("March")
		self.setGeometry(0, 0, 1024, 768)
		self.setLayout(layout)

