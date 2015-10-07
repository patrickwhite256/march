#!/usr/bin/env python

#
# Testing audio
#

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSignal, QUrl, QFile, QFileInfo, QTime, QDir
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout,
        QVBoxLayout, QHBoxLayout, QToolButton, QLineEdit, QFileDialog)


# *
# This widget contains both the ogg file selector widget, and the
# sample interval selector/player widget. Together they make...
# MusicSampleWidget!!!
# *
class MusicSampleWidget(QWidget):
    def __init__(self, parent=None):
        super(MusicSampleWidget, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        song_select = SongSelectWidget()
        interval_edit = IntervalEditWidget()

        song_select.new_song_selected.connect(interval_edit.new_song)

        layout = QVBoxLayout()
        layout.addWidget(song_select)
        layout.addWidget(interval_edit)
        self.setLayout(layout)


# *
# This widget contains a file selector button to bring up a dialog,
# and a label indicating the current song.
# *
class SongSelectWidget(QWidget):

    new_song_selected = pyqtSignal(['QFile'])

    def __init__(self, parent=None):
        super(SongSelectWidget, self).__init__(parent)

        self.audio_file = QFile()
        self.init_dialog()
        self.init_ui()

    def init_dialog(self):
        self.file_dialog = QFileDialog(
            fileSelected=self.set_audio_file
        )
        self.file_dialog.setNameFilter("Ogg Audio (*.ogg)")
        self.file_dialog.selectFile(
            self.audio_file.fileName()
        )

    def init_ui(self):
        self.file_button = QToolButton(
            clicked=self.open_dialog
        )
        self.file_button.setText("Select New Audio File")
        short_name = QFileInfo(self.audio_file).fileName()
        self.nameLabel = QLabel(
            "File: " + short_name
        )

        layout = QVBoxLayout()
        layout.addWidget(self.file_button)
        layout.addWidget(self.nameLabel)
        self.setLayout(layout)

    def open_dialog(self):
        self.file_dialog.exec()

    def set_audio_file(self, file_path):
        self.audio_file = QFile(file_path)
        short_name = QFileInfo(self.audio_file).fileName()
        self.nameLabel.setText(
            "File: " + short_name
        )
        self.new_song_selected.emit(self.audio_file)

    def get_audio_file():
        return self.audio_file


# *
# IntervalEditWidget. Given an ogg file, play the interval specified.
# No special rules as of yet, really.
# *
class IntervalEditWidget(QWidget):

    play_interval = pyqtSignal()
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self, parent=None):
        super(IntervalEditWidget, self).__init__(parent)

        # TODO Make player support StoppedState, interval player only available
        # when in StoppedState
        self.playerState = QMediaPlayer.StoppedState

        self.init_ui()
        self.init_player()

    def init_ui(self):
        mainLayout = QGridLayout()

        self.init_buttons()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.intervalButton)
        mainLayout.addLayout(buttonLayout, 0, 0)
        mainLayout.addWidget(self.startLabel, 1, 0)
        mainLayout.addWidget(self.endLabel, 1, 1)
        mainLayout.addWidget(self.startTime, 2, 0)
        mainLayout.addWidget(self.endTime, 2, 1)

        self.setLayout(mainLayout)

    def init_buttons(self):
        self.playButton = QToolButton(clicked=self.playPressed)
        self.playButton.setText("play")

        self.stopButton = QToolButton(clicked=self.stopPressed)
        self.stopButton.setText("stop")

        self.intervalButton = QToolButton(clicked=self.intervalPressed)
        self.intervalButton.setText("play interval")

        self.startLabel = QLabel("Start Time (s):")
        self.startTime = QLineEdit()
        self.startTime.setValidator(QDoubleValidator())
        self.startTime.setText('0.0')

        self.endLabel = QLabel("Duration (s):")
        self.endTime = QLineEdit()
        self.endTime.setValidator(QDoubleValidator())
        self.endTime.setText('0.0')

    def init_player(self):
        self.timeLabel = QLabel("")

        self.media_player = QMediaPlayer()
        self.media_player.setNotifyInterval(17)  # ms ie. ~60hz
        self.media_player.stop()
        self.playlist = QMediaPlaylist()
        self.media_player.setPlaylist(self.playlist)
        self.media_player.pause()

        self.media_player.positionChanged.connect(self.positionChanged)
        self.intervalEnd = None  # initialize this

        self.setState(self.media_player.state())
        self.play.connect(self.media_player.play)
        self.pause.connect(self.media_player.pause)
        self.stop.connect(self.media_player.stop)
        self.play_interval.connect(self.playInterval)

    def state(self):
        return self.playerState

    def setState(self, state):
        if state != self.playerState:
            self.playerState = state

            if state == QMediaPlayer.PlayingState:
                self.playButton.setText("pause")
            else:
                self.playButton.setText("play")

    def getInterval(self):
        return float(self.startTime.text()), float(self.endTime.text())

    def new_song(self, new_file):
        self.playlist.clear()
        media_content = QMediaContent(QUrl("file:"+new_file.fileName()))
        self.playlist.addMedia(media_content)

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
            print("player not stopped, won't play interval")
            return
        self.setState(QMediaPlayer.PlayingState)
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

    def playInterval(self):
        # remember, position is in milliseconds and always accessible
        # self.media_player.position
        # first we need the start and duration
        start, duration = self.getInterval()
        start = start * 1000
        duration = duration * 1000
        self.intervalEnd = start + duration
        self.media_player.setPosition(start)
        self.media_player.play()
        self.setState(QMediaPlayer.PlayingState)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    music_info_w = MusicSampleWidget()
    music_info_w.show()

    sys.exit(app.exec_())
