from PyQt5.QtGui import QDoubleValidator, QIcon
from PyQt5.QtCore import pyqtSignal, QUrl, QFile, QFileInfo, QTime, QDir, QRect
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout,
        QVBoxLayout, QHBoxLayout, QToolButton, QLineEdit, QFileDialog,
        QSizePolicy, QFrame)


class MarchSongSelectView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setContentsMargins(2, 2, 2, 2)  # just something smaller, imo
        self.setMaximumHeight(384)  # 768/3
        self.setMaximumWidth(224)  # 1024/4 ( accually, less is better )

        songSelect = SongSelectWidget()
        intervalEdit = IntervalEditWidget()

        songSelect.newSongSelected.connect(intervalEdit.newSong)

        layout = QVBoxLayout()
        layout.addWidget(songSelect)
        layout.addWidget(intervalEdit)
        self.setLayout(layout)


class SongSelectWidget(QWidget):

    newSongSelected = pyqtSignal(['QFile'])

    def __init__(self, parent=None):
        super(SongSelectWidget, self).__init__(parent)

        self.audioFile = QFile()
        self.initDialog()
        self.initUI()

    def initDialog(self):
        self.fileDialog = QFileDialog(fileSelected=self.setAudioFile)
        self.fileDialog.setNameFilter("Ogg Audio (*.ogg)")
        self.fileDialog.selectFile(self.audioFile.fileName())

    def initUI(self):
        self.fileButton = QToolButton(clicked=self.openDialog)
        self.fileButton.setText("Select New Audio File")
        shortName = QFileInfo(self.audioFile).fileName()
        self.nameLabel = QLabel("File: " + shortName)

        layout = QVBoxLayout()
        layout.addWidget(self.fileButton)
        layout.addWidget(self.nameLabel)
        self.setLayout(layout)

    def openDialog(self):
        self.fileDialog.exec()

    def setAudioFile(self, filePath):
        self.audioFile = QFile(filePath)
        shortName = QFileInfo(self.audioFile).fileName()
        self.nameLabel.setText("File: " + shortName)
        self.newSongSelected.emit(self.audioFile)

    def getAudioFile():
        return self.audioFile


# TODO - actually clean up what needs to be self.x vs. just x
class IntervalEditWidget(QWidget):

    play_interval = pyqtSignal()
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super(IntervalEditWidget, self).__init__(parent)

        self.playerState = QMediaPlayer.StoppedState

        self.initUI()
        self.initPlayer()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.initButtons()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.intervalButton)
        mainLayout.addLayout(buttonLayout)

        labelLayout = QGridLayout()
        labelLayout.addWidget(self.startLabel, 1, 0)
        labelLayout.addWidget(self.endLabel, 1, 1)
        labelLayout.addWidget(self.startTime, 2, 0)
        labelLayout.addWidget(self.endTime, 2, 1)
        mainLayout.addLayout(labelLayout)

        self.setLayout(mainLayout)

    def initButtons(self):
        self.playButton = QToolButton(clicked=self.playPressed)
        self.playButton.setIcon(QIcon.fromTheme("media-playback-start"))

        self.stopButton = QToolButton(clicked=self.stopPressed)
        self.stopButton.setIcon(QIcon.fromTheme("media-playback-stop"))

        self.intervalButton = QToolButton(clicked=self.intervalPressed)
        self.intervalButton.setText("Play Sample")

        self.startLabel = QLabel("Start Time (s):")
        self.startTime = QLineEdit()
        self.startTime.setValidator(QDoubleValidator())
        self.startTime.setText('0.0')

        self.endLabel = QLabel("Duration (s):")
        self.endTime = QLineEdit()
        self.endTime.setValidator(QDoubleValidator())
        self.endTime.setText('12.0')  # default time: 12s, standard

    def initPlayer(self):
        self.timeLabel = QLabel("")

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setNotifyInterval(17)  # ms ie. ~60hz
        self.mediaPlayer.stop()
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)
        self.mediaPlayer.pause()

        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.intervalEnd = None  # initialize this

        self.setState(self.mediaPlayer.state())
        self.play.connect(self.mediaPlayer.play)
        self.pause.connect(self.mediaPlayer.pause)
        self.stop.connect(self.mediaPlayer.stop)
        self.play_interval.connect(self.playInterval)

    def state(self):
        return self.playerState

    def setState(self, state):
        if state != self.playerState:
            self.playerState = state

            if state == QMediaPlayer.PlayingState:
                self.playButton.setIcon(QIcon.fromTheme("media-playback-pause"))
            else:
                self.playButton.setIcon(QIcon.fromTheme("media-playback-start"))

    def getInterval(self):
        return float(self.startTime.text()), float(self.endTime.text())

    def newSong(self, newFile):
        self.playlist.clear()
        mediaContent = QMediaContent(QUrl("file:"+newFile.fileName()))
        self.playlist.addMedia(mediaContent)

    # PROBLEM/TODO: segfault when close after pressing play to start song?
    def playPressed(self):
        if self.playerState == QMediaPlayer.PlayingState:
            self.setState(QMediaPlayer.PausedState)
            self.pause.emit()
        else:
            self.setState(QMediaPlayer.PlayingState)
            self.play.emit()

    def stopPressed(self):
        self.setState(QMediaPlayer.StoppedState)
        self.stop.emit()

    def intervalPressed(self):
        if not self.playerState == QMediaPlayer.StoppedState:
            return
        self.play_interval.emit()

    def positionChanged(self, progress):
        self.updateDurationInfo(progress/1000)  # because ms

        if(self.intervalEnd and progress >= self.intervalEnd):
            self.setState(QMediaPlayer.StoppedState)
            self.stop.emit()
            self.intervalEnd = None  # idk maybe something less shitty

    def updateDurationInfo(self, currentInfo):
        if currentInfo:
            currentTime = QTime((currentInfo/3600) % 60, (currentInfo/60) % 60,
                    currentInfo % 60, (currentInfo*1000) % 1000)
            format = 'hh:mm:ss'
            tStr = currentTime.toString(format)
            self.timeLabel.setText(tStr)
        else:
            tStr = ""

        self.timeLabel.setText(tStr)
<<<<<<< HEAD
=======

    def playInterval(self):
        start, duration = self.getInterval()
        start = start * 1000
        duration = duration * 1000

        # setting intervalEnd will cause it to check whether
        # it's passed intervalEnd on positionChanged
        self.intervalEnd = start + duration
        self.mediaPlayer.setPosition(start)
        self.mediaPlayer.play()
        self.setState(QMediaPlayer.PlayingState)
>>>>>>> ed8e2b6... cleaning up a bit, still getting segfault
