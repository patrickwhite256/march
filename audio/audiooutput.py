#!/usr/bin/env python

#############################################################################
#
# Testing audio shit - Kelly McBride 2015
#
#
#############################################################################


from PyQt5.QtCore import pyqtSignal, QUrl, QFileInfo, QTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout,
        QVBoxLayout, QToolButton)


class AudioControl(QWidget):

    play = pyqtSignal()
    pause = pyqtSignal()

    def __init__(self, parent=None):
        super(AudioControl, self).__init__(parent)

        self.playerState = QMediaPlayer.PausedState

        # give it buttons that will be useful
        # this button should toggle play and pause
        self.playButton = QToolButton(clicked=self.playPressed)
        self.playButton.setText("play")

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.playButton, 1, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Shitty Audio Player???")

    def state(self):
        return self.playerState

    def setState(self, state):
        if state != self.playerState:
            self.playerState = state

            if state == QMediaPlayer.PausedState:
                self.playButton.setText("play")
            elif state == QMediaPlayer.PlayingState:
                self.playButton.setText("pause")

    def playPressed(self):
        if self.playerState == QMediaPlayer.PausedState:
            print("player state is paused.")
            self.play.emit()
        elif self.playerState == QMediaPlayer.PlayingState:
            print("player state is playing.")
            self.pause.emit()
        else:
            print("player state is neither paused nor playing.")
            print("Player state", self.playerState)


class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(parent)

        # MY CODE
        # replace with file selector (eventually)
        audio_file_name = "juliet.ogg"
        self.nameLabel = QLabel("File: " + audio_file_name)
        self.timeLabel = QLabel("00:00:00")

        fname = QFileInfo(audio_file_name).absoluteFilePath()
        url = QUrl.fromLocalFile(fname)
        media_content = QMediaContent(url)

        self.media_player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(media_content)
        self.media_player.setPlaylist(self.playlist)
        self.media_player.pause()

        self.media_player.positionChanged.connect(self.positionChanged)

        controls = AudioControl()
        controls.setState(self.media_player.state())
        controls.play.connect(self.media_player.play)
        controls.pause.connect(self.media_player.pause)

        layout = QVBoxLayout()
        layout.addWidget(controls)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.timeLabel)
        self.setLayout(layout)

        # self.media_player.play()

    def positionChanged(self, progress):
        progress /= 1000  # because milliseconds, i think
        self.updateDurationInfo(progress)

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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    audio_player = AudioPlayer()
    audio_player.show()

    sys.exit(app.exec_())
