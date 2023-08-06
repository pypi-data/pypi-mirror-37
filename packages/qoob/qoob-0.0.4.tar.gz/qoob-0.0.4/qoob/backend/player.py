#!/usr/bin/python3
from PyQt5 import QtWidgets, QtCore, QtMultimedia

try:
    import qoob.backend.parser as parser
except ImportError:
    import backend.parser as parser


class MediaPlayer(QtMultimedia.QMediaPlayer):
    popup = QtCore.pyqtSignal(str)
    setItemColor = QtCore.pyqtSignal(str)
    setSliderRange = QtCore.pyqtSignal(int, int)
    setSliderValue = QtCore.pyqtSignal(int)
    setPlayPauseIcon = QtCore.pyqtSignal(object)
    setShuffleIcon = QtCore.pyqtSignal(object)
    setWindowTitle = QtCore.pyqtSignal(str)
    setStatusMessage = QtCore.pyqtSignal(str, str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.icon = parent.icon
        self.preferences = parent.preferences
        self.mediaStatusChanged.connect(self._mediaChangedEvent)
        self.durationChanged.connect(self._updateDuration)
        self.positionChanged.connect(self._updateSlider)
        self.seekableChanged.connect(self._seekableEvent)
        self.random = QtCore.QRandomGenerator()
        self.playLater = QtCore.QTimer(singleShot=True, interval=500)
        self.playLater.timeout.connect(self.nextEvent)

        self.lastPlayed = []
        self.lastItem = None
        self.shuffle = False
        self.mediaLength = "?"
        self.path = ""

        self.statusTimer = QtCore.QTimer(interval=500)
        self.statusTimer.timeout.connect(self._updateStatus)
        self.statusTimer.start()

    def _currentItem(self):
        return self.parent.tabWidget.current.currentItem()

    def _currentTab(self):
        return self.parent.tabWidget.current

    def _mediaChangedEvent(self, event):
        if event == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.nextEvent()
        elif event == QtMultimedia.QMediaPlayer.InvalidMedia:
            self.setItemColor.emit("red")
            self.setStatusMessage.emit(self.path, "Invalid media")
            self.playLater.start()  # Cannot call nextEvent directly (too fast)

    def _seekableEvent(self):
        if self.resumePlayback and self.isSeekable():
            self.resumePlayback = False
            self.setPosition(self.preferences.get("state", "playback position"))

    def _setCurrentItem(self, item):
        # Slots/signals too slow, sync required
        self._currentTab().setCurrentItem(item)

    def _shuffleNext(self):
        currentRow = self._currentTab().currentIndex().row()
        itemCount = self._currentTab().topLevelItemCount()

        if len(self.lastPlayed) == itemCount:
            self.stopEvent()
            self.lastPlayed = []
        elif itemCount > 1:
            next = self._shuffleTrack(itemCount)
            self._setCurrentItem(next)
            self.activateSelection()
            self.lastPlayed.append(currentRow)

    def _shuffleTrack(self, count):
        next = self.random.bounded(count)
        while next in self.lastPlayed:
            next = self.random.bounded(count)
        return self._currentTab().topLevelItem(next)

    def _titleFormat(self, title):
        replace = ("artist", "album", "track", "title")
        for tag in replace:
            title = title.replace("%" + tag + "%", self.tags[tag])
        return title

    def _updateDuration(self, duration):
        s = duration / 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        self.mediaLength = "%02d:%02d:%02d" % (h, m, s)
        self.setSliderRange.emit(0, self.duration())

    def _updateSlider(self, progress):
        if not self.parent.ui.slider.isSliderDown():
            self.setSliderValue.emit(progress)

    def _updateStatus(self):
        if self.duration() > -1:
            if self.state() == QtMultimedia.QMediaPlayer.PlayingState:
                left = "Now playing: " + self.tags["title"] + " (" + self.tags["artist"] + ")"
            elif self.state() == QtMultimedia.QMediaPlayer.PausedState:
                left = "Paused"
            elif self.state() == QtMultimedia.QMediaPlayer.StoppedState:
                left = "Stopped"

            s = self.parent.ui.slider.value() / 1000
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)
            elapsed = "%02d:%02d:%02d" % (h, m, s)
            right = f"    {elapsed} / {self.mediaLength}"
            self.setStatusMessage.emit(left, right)

    def activateSelection(self):
        self.resumePlayback = False
        if self.lastItem:
            self.lastItem.setColor("none")

        if self._currentItem():
            self._currentItem().setColor("green")
            self.setCurrentMedia(self._currentItem().text(5))
            self.lastItem = self._currentItem()
            title = self._titleFormat(self.preferences.get("viewer", "notification format"))
            self.popup.emit(title)

        elif self._currentTab().topLevelItemCount() > 0:
            first = self._currentTab().topLevelItem(0)
            self._currentTab().setCurrentItem(first)
            self._setCurrentItem(first)
            self.lastPlayed.append(self._currentTab().currentIndex().row())
            self.activateSelection()

    def clearPlaylist(self):
        self.lastPlayed = []

    def nextEvent(self):
        currentRow = self._currentTab().currentIndex().row()
        itemCount = self._currentTab().topLevelItemCount()
        if self._currentItem():
            if self.shuffle:
                self._shuffleNext()
            elif currentRow == itemCount - 1:
                self.stopEvent()
            else:
                next = self._currentTab().itemBelow(self._currentItem())
                self._setCurrentItem(next)
                self.activateSelection()
                self.lastPlayed.append(currentRow)
        else:
            self.activateSelection()

    def pauseEvent(self):
        self.playLater.stop()
        self.pause()
        self.setPlayPauseIcon.emit(self.icon["play"])

    def playEvent(self):
        self.playLater.stop()
        if self.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.play()
            self.setPlayPauseIcon.emit(self.icon["pause"])

        elif self.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self.activateSelection()

    def playPauseEvent(self):
        self.playLater.stop()
        if self.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.pauseEvent()
        else:
            self.playEvent()

    def previousEvent(self):
        self.playLater.stop()
        if self._currentItem():
            if self.lastPlayed:
                previous = self.lastPlayed.pop()
                previous = self._currentTab().topLevelItem(previous)
            else:
                previous = self._currentTab().itemAbove(self._currentItem())
                if not previous:
                    previous = self._currentTab().topLevelItem(0)
            self._setCurrentItem(previous)
        self.activateSelection()

    def setCurrentMedia(self, path):
        self.path = path
        self.media = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path))
        self.setMedia(self.media)
        self.play()
        self.setPlayPauseIcon.emit(self.icon["pause"])
        strip = self.preferences.get("viewer", "strip titles")
        self.tags = self.parent.parser.header(self.path)
        title = self._titleFormat(self.preferences.get("viewer", "title format"))
        self.setWindowTitle.emit(title)
        if "error" in self.tags:
            self.setItemColor.emit("yellow")
            self.setStatusMessage.emit(self.path, self.tags["error"])

    def shuffleEvent(self, checked=False, enable=None):
        self.shuffle = not self.shuffle if enable is None else enable
        if self.shuffle:
            self.setShuffleIcon.emit(self.icon["shuffle_on"])
        else:
            self.setShuffleIcon.emit(self.icon["shuffle_off"])

    def stopEvent(self):
        self.stop()
        self.playLater.stop()
        self.lastPlayed = []
        self.setSliderValue.emit(0)
        self.setPlayPauseIcon.emit(self.icon["play"])
