from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from .info_view import MarchInfoView
from .song_view import MarchSongSelectView
from .nav_view import MarchNavigationView
from .track_view import MarchTrackView
from .note_view import MarchNoteView

class MarchSideBarView(QFrame):
	def __init__(self, parent):
		super(MarchSideBarView, self).__init__(parent)
		self.initUI()
	
	def initUI(self):
		self.setFrameStyle(QFrame.Box)
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
		self.layout = QVBoxLayout()

		self.setLayout(self.layout)

	def addView(self, view):
		self.layout.addWidget(view)


# Main Window
class MarchWindow(QWidget):
	
	def __init__(self):
		super(MarchWindow, self).__init__()

		self.initUI()

	
	def initUI(self):
		layout = QGridLayout()
		leftSideBar = MarchSideBarView(self)
		infoView = MarchInfoView(leftSideBar)
		songView = MarchSongSelectView(leftSideBar)
		navView = MarchNavigationView(leftSideBar)

		leftSideBar.addView(infoView)
		leftSideBar.addView(songView)
		leftSideBar.addView(navView)
		
		rightSideBar = MarchSideBarView(self)
		noteView = MarchNoteView(rightSideBar)

		rightSideBar.addView(noteView)

		layout.addWidget(leftSideBar, 0, 0)
		layout.addWidget(MarchTrackView(self), 0, 1, 1, 2)
		layout.addWidget(rightSideBar, 0, 4)
		
		self.setWindowTitle("March")
		self.setGeometry(0, 0, 1024, 768)
		self.setLayout(layout)

