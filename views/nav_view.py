from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QVBoxLayout,
        QHBoxLayout, QSizePolicy)


# *
# NavigationView. ie, enter a bar & beat and jump to that place.
# Maybe should have a "jump" button?
# TrackView has self.column, self.row -> row has beat & bar
# *
class MarchNavigationView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout = QVBoxLayout()

        barLayout = QHBoxLayout()
        self.barLabel = QLabel("Active Measure:")
        self.barBox = QLineEdit()
        barLayout.addWidget(self.barLabel)
        barLayout.addWidget(self.barBox)

        beatLayout = QHBoxLayout()
        self.beatLabel = QLabel("Active Beat:")
        self.beatBox = QLineEdit()
        beatLayout.addWidget(self.beatLabel)
        beatLayout.addWidget(self.beatBox)

        self.layout.addLayout(barLayout)
        self.layout.addLayout(beatLayout)

        self.setLayout(self.layout)
