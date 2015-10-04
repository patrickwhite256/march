#!/usr/bin/env python

#
# Testing audio
#

from PyQt5.QtCore import pyqtSignal, QUrl, QFileInfo, QTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout,
        QVBoxLayout, QHBoxLayout, QToolButton, QLineEdit)


class AudioControl(QWidget):

    play = pyqtSignal()
    play_interval = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super(AudioControl, self).__init__(parent)

        # TODO Make player support StoppedState, interval player only available
        # when in StoppedState
        self.playerState = QMediaPlayer.StoppedState

        # this button should toggle play and pause
        self.playButton = QToolButton(clicked=self.playPressed)
        self.playButton.setText("play")

        # stop button
        self.stopButton = QToolButton(clicked=self.stopPressed)
        self.stopButton.setText("stop")

        # play_interval button
        self.intervalButton = QToolButton(clicked=self.intervalPressed)
        self.intervalButton.setText("play interval")

        # TODO validators on these fields.
        # - ints (or floats? they could potentially have decimals)
        # - not greater than song length
        # - not less than 0
        self.startLabel = QLabel("Start Time (s):")
        self.startTime = QLineEdit()
        self.startTime.setText('0')

        self.endLabel = QLabel("End Time (s):")
        self.endTime = QLineEdit()
        self.endTime.setText('0')

        mainLayout = QGridLayout()

        stdButtonLayout = QHBoxLayout()
        stdButtonLayout.addWidget(self.playButton)
        stdButtonLayout.addWidget(self.stopButton)
        stdButtonLayout.addWidget(self.intervalButton)
        mainLayout.addLayout(stdButtonLayout, 0, 0)
        mainLayout.addWidget(self.startLabel, 1, 0)
        mainLayout.addWidget(self.endLabel, 1, 1)
        mainLayout.addWidget(self.startTime, 2, 0)
        mainLayout.addWidget(self.endTime, 2, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Audio Player???")

    def state(self):
        return self.playerState

    def setState(self, state):
        if state != self.playerState:
            self.playerState = state

            if state in (QMediaPlayer.PausedState, QMediaPlayer.StoppedState):
                self.playButton.setText("play")
            elif state == QMediaPlayer.PlayingState:
                self.playButton.setText("pause")

    def getInterval(self):
        return int(self.startTime.text()), int(self.endTime.text())

    # TODO is it just me or is this grody? ^, then v. grody if/elif
    def playPressed(self):
        if self.playerState in (QMediaPlayer.PausedState, QMediaPlayer.StoppedState):
            self.setState(QMediaPlayer.PlayingState)
            print("player state now playing.")
            self.play.emit()
        elif self.playerState == QMediaPlayer.PlayingState:
            self.setState(QMediaPlayer.PausedState)
            print("player state now paused.")
            self.pause.emit()

    def stopPressed(self):
        self.setState(QMediaPlayer.StoppedState)
        print("player state now stopped.")
        self.stop.emit()

    def intervalPressed(self):
        if not self.playerState == QMediaPlayer.StoppedState:
            print("player not stopped, won't play interval")
            return
        self.setState(QMediaPlayer.PlayingState)
        print("playing interval")
        self.play_interval.emit()


class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(parent)

        # MY CODE
        self.init_player()

        self.controls = AudioControl()
        self.controls.setState(self.media_player.state())
        self.controls.play.connect(self.media_player.play)
        self.controls.pause.connect(self.media_player.pause)
        self.controls.stop.connect(self.media_player.stop)
        self.controls.play_interval.connect(self.playInterval)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.controls)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.timeLabel)
        self.setLayout(layout)

    def init_player(self):
        # replace with file selector (eventually)
        audio_file_name = "audio/juliet.ogg"
        self.nameLabel = QLabel("File: " + audio_file_name)
        self.timeLabel = QLabel("00:00:00")

        fname = QFileInfo(audio_file_name).absoluteFilePath()
        url = QUrl.fromLocalFile(fname)
        media_content = QMediaContent(url)

        self.media_player = QMediaPlayer()
        self.media_player.stop()
        self.media_player.setNotifyInterval(50)  # ms
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(media_content)
        self.media_player.setPlaylist(self.playlist)
        self.media_player.pause()

        self.media_player.positionChanged.connect(self.positionChanged)
        self.intervalEnd = None  # initialize this

    def positionChanged(self, progress):
        self.updateDurationInfo(progress/1000)  # because ms

        if(self.intervalEnd and progress >= self.intervalEnd):
            self.media_player.stop()
            self.controls.setState(QMediaPlayer.StoppedState)
            self.intervalEnd = None  # idk maybe something less shitty

    def updateDurationInfo(self, currentInfo):
        if currentInfo:
            currentTime = QTime((currentInfo/3600) % 60, (currentInfo/60) % 60,
                    currentInfo % 60, (currentInfo*1000) % 1000)
            format = 'hh:mm:ss'
            tStr = currentTime.toString(format)
            self.timeLabel.setText(tStr)
        else:
            tStr = " ___ "

        self.timeLabel.setText(tStr)

    def playInterval(self):
        # remember, position is in milliseconds and always accessible
        # self.media_player.position
        # first we need the start and end
        start, end = self.controls.getInterval()
        start = start * 1000
        end = end * 1000
        self.intervalEnd = end
        self.media_player.setPosition(start)
        self.media_player.play()
        self.controls.setState(QMediaPlayer.PlayingState)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    audio_player = AudioPlayer()
    audio_player.show()

    sys.exit(app.exec_())
