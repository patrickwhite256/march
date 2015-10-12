from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette
from models import Note, Tap, Hold
from .arrow_label import MarchArrowLabel, MarchBombLabel, MarchHoldLabel

class MarchNoteLabel(QWidget):

    selected = pyqtSignal()

    def __init__(self, note_type, parent):
        super().__init__(parent)
        self.note_type = note_type
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.text_label = QLabel(self)

        if (self.note_type == Tap.TYPE_NORMAL):
            self.text_label.setText('Normal Arrow')
            self.arrow_label = MarchArrowLabel(Note.POSITION_UP, self)
        elif (self.note_type == Tap.TYPE_MINE):
            self.text_label.setText('Mine')
            self.arrow_label = MarchBombLabel(self)
        elif (self.note_type == Hold.TYPE_HOLD):
            self.text_label.setText('Hold Note')
            self.arrow_label = MarchHoldLabel(Hold.TYPE_HOLD, self)
        elif (self.note_type == Hold.TYPE_ROLL):
            self.text_label.setText('Roll Note')
            self.arrow_label = MarchHoldLabel(Hold.TYPE_ROLL, self)

        self.layout.addWidget(self.arrow_label)
        self.layout.addWidget(self.text_label)
        self.setLayout(self.layout) 

        
    def setSelected(self, selected):
        qpal = QPalette()
        qpal.setColor(QPalette.Background, Qt.cyan)
        self.setAutoFillBackground(true)
        self.setPalette(qpal)
        self.show() 

    # Event Handlers

    def mousePressEvent(self, event):
        self.selected()
        
