from PyQt5.QtWidgets import (QWidget, QFrame, QHBoxLayout, QVBoxLayout, 
                            QSizePolicy, QGridLayout, QLabel, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from .note_label import MarchNoteLabel
from models import Tap, Hold
    
class MarchNoteView(QWidget):

    selectionChange = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.child_labels = [];
        self.initUI()
        
        for label in self.child_labels:
            label.selected.connect(self.childSelectedEvent)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.group_box = QGroupBox(self)
        self.group_box.setTitle("Add Notes")

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.normal_label = MarchNoteLabel(Tap.TYPE_NORMAL, self)
        self.mine_label = MarchNoteLabel(Tap.TYPE_MINE, self)
        self.hold_label = MarchNoteLabel(Hold.TYPE_HOLD, self)
        self.roll_label = MarchNoteLabel(Hold.TYPE_ROLL, self)

        self.layout.addWidget(self.normal_label)
        self.layout.addWidget(self.mine_label)
        self.layout.addWidget(self.hold_label)
        self.layout.addWidget(self.roll_label)

        self.child_labels.append(self.normal_label)
        self.child_labels.append(self.mine_label)
        self.child_labels.append(self.hold_label)
        self.child_labels.append(self.roll_label)

        self.group_box.setLayout(self.layout) 
    
    # Event Handlers

    def childSelectedEvent(self, event):
        for label in [label for label in self.child_labels if label.note_type != event]:
            label.setSelected(False)

        self.selectionChange.emit(event)
        

