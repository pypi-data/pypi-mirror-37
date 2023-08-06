#!/usr/bin/python3
import os
import sys
from contextlib import suppress
from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia, uic

try:
    import qoob.backend.tools as tools
    import qoob.backend.player as player
    import qoob.backend.parser as parser
    import qoob.frontend.preferences as preferences
    import qoob.frontend.trinkets as trinkets
    import qoob.frontend.playlist as playlist
    import qoob.ui.player
except ImportError:
    import backend.tools as tools
    import backend.player as player
    import backend.parser as parser
    import frontend.preferences as preferences
    import frontend.trinkets as trinkets
    import frontend.playlist as playlist

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
DB_DIR = os.path.expanduser("~/.config/qoob/")


class LibraryTree(QtWidgets.QTreeWidget):
    selectedItem = QtCore.pyqtSignal()
    clearFilter = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.preferences = parent.preferences
        self.libraryView = parent.tabWidget.tabs["Library viewer"]["playlist"]
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setIndentation(10)
        self.header().setVisible(False)
        self.itemSelectionChanged.connect(self._selectItem)

    def _hasFilteredFiles(self, path):
        for root, subfolders, files in os.walk(path):
            for f in files:
                if parser.allowedType(f):
                    if self._sift(f):
                        return True
        return False

    def _recursiveScan(self, folder, node=None):
        try:
            for f in os.listdir(folder):
                path = os.path.join(folder, f)
                if os.path.isdir(path):
                    if self._hasFilteredFiles(path):
                        item = self.addItem(node, path)
                        self._recursiveScan(path, node=item)

                elif parser.allowedType(path):
                    if self._sift(f):
                        self.addItem(node, path)
        except PermissionError:
            pass

    def _scanSelection(self, path):
        for root, subfolder, files in os.walk(path):
            for f in files:
                if self._sift(f):
                    self.libraryView.add(os.path.join(root, f))
        if os.path.isfile(path):
            if self._sift(path):
                self.libraryView.add(path)

    def _selectItem(self):
        self.libraryView.clear()
        for item in self.selectedItems():
            if item.text(1):
                self._scanSelection(item.text(1))
            elif item.text(0) == "All Music":
                for folder in self.preferences.get("music database"):
                    self._scanSelection(folder)
        self.selectedItem.emit()

    def _sift(self, string):
        sift = self.parent.ui.libraryFilterLine.text()
        return string.lower().count(sift.lower()) > 0

    def addArtist(self, node):
        self.addTopLevelItem(node)
        self.sortItems(0, QtCore.Qt.AscendingOrder)

    def addItem(self, node, path):
        name = os.path.splitext(os.path.basename(path))[0]
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, path)
        if node:
            node.addChild(item)
        else:
            self.addTopLevelItem(item)
        return item

    def addWildCard(self):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "All Music")
        self.insertTopLevelItem(0, item)

    def clearAll(self):
        self.clearFilter.emit()
        self.clear()

    """
    def deleteItem(self, item, path):
        for subItem in range(item.childCount()):
            subItem = item.child(subItem)
            if subItem.childCount() > 0:
                self.deleteItem(subItem, path)
            elif subItem.text(1) == path:
                index = item.indexOfChild(subItem)
                item.takeChild(index)
                return True
        return False
    """

    def filterEvent(self):
        self.refresh()
        if self.preferences.get("viewer", "expand library"):
            count = self.topLevelItemCount()
            for item in range(self.topLevelItemCount()):
                count += self.topLevelItem(item).childCount()
            if (count * 12) <= self.height():  # Where 12px is the height of one item
                self.expandAll()

    def refresh(self):
        self.clear()
        for folder in self.preferences.get("music database"):
            self._recursiveScan(folder)
        self.addWildCard()


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        if "qoob.ui.player" in sys.modules:
            self.ui = qoob.ui.player.Ui_MainWindow()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + "ui/player.ui", self)

        self.copied = []
        self._initStyle()

        self.parent = parent
        self.logger = tools.Logger(name="qoob", path=DB_DIR)
        self.log = self.logger.new("qoob")
        self.preferences = preferences.PreferencesDatabase(self)
        self.preferencesForm = preferences.PreferencesForm(self)
        self.popup = trinkets.PopupWidget(self)
        self.process = QtCore.QProcess()
        self.random = QtCore.QRandomGenerator()
        if not self.preferences.db["music database"]:
            self._findDefaultMusicFolder()

        self.player = player.MediaPlayer(self)
        self.parser = parser.Parser(self)
        self.tabWidget = playlist.Tabs(self)
        self.library = LibraryTree(self)
        self.trayIcon = trinkets.TrayIcon(self)

        self.player.popup.connect(self.popup.display)
        self.player.setItemColor.connect(self.setItemColor)
        self.player.setSliderRange.connect(self.ui.slider.setRange)
        self.player.setSliderValue.connect(self.ui.slider.setValue)
        self.player.setPlayPauseIcon.connect(self.ui.playButton.setIcon)
        self.player.setShuffleIcon.connect(self.ui.shuffleButton.setIcon)
        self.player.setWindowTitle.connect(self.setWindowTitle)
        self.player.setStatusMessage.connect(self.setStatusMessage)

        self.tabWidget.action.connect(self.action)
        self.tabWidget.play.connect(self.player.playPauseEvent)
        self.tabWidget.changed.connect(self.player.clearPlaylist)
        self.library.selectedItem.connect(self.librarySelect)
        self.library.clearFilter.connect(self.ui.libraryFilterLine.clear)
        self.preferencesForm.accepted.connect(self.preferencesSave)
        self.preferencesForm.resetMetadata.connect(self.parser.reset)
        self.preferencesForm.activateWindow()

        self.parserThread = QtCore.QThread()
        self.parserThread.started.connect(self.parser.scanAll)
        self.parser.moveToThread(self.parserThread)
        self.parser.done.connect(self.libraryDone)
        self.parser.addArtist.connect(self.library.addArtist)
        self.parser.addAlbum.connect(self.library.addItem)
        self.parser.clear.connect(self.library.clearAll)
        self.parser.startDb.connect(self.preferencesForm.dbStartSlot)
        self.parser.doneDb.connect(self.preferencesForm.dbDoneSlot)
        self.parser.pending.connect(self.preferencesForm.setPending)
        self.parser.setFilterEnable.connect(self.ui.libraryFilterLine.setEnabled)
        self.parserThread.start()

        self.trayIcon.hideWindow.connect(self.hide)
        self.trayIcon.showWindow.connect(self.show)
        self.trayIcon.close.connect(self.close)
        self.trayIcon.play.connect(self.player.playPauseEvent)
        self.trayIcon.stop.connect(self.player.stopEvent)
        self.trayIcon.next.connect(self.player.nextEvent)
        self.trayIcon.previous.connect(self.player.previousEvent)
        self.trayIcon.shuffle.connect(self.player.shuffleEvent)
        self.trayIcon.showPreferencesForm.connect(self.preferencesForm.show)
        self.trayIcon.popup.connect(self.popup.display)

        self.menu = QtWidgets.QMenu()
        self.menu.aboutToShow.connect(self._menuRefresh)

        self.ui.statusBar = QtWidgets.QStatusBar()
        self.ui.statusRightLabel = QtWidgets.QLabel()

        self.ui.statusBar.addPermanentWidget(self.ui.statusRightLabel)
        self.ui.libraryLayout.insertWidget(0, self.library)
        self.ui.tabLayout.addWidget(self.tabWidget, 1, 1, 1, 6)

        self.ui.playButton.clicked.connect(self.player.playPauseEvent)
        self.ui.stopButton.clicked.connect(self.player.stopEvent)
        self.ui.nextButton.clicked.connect(self.player.nextEvent)
        self.ui.previousButton.clicked.connect(self.player.previousEvent)
        self.ui.shuffleButton.clicked.connect(self.player.shuffleEvent)
        self.ui.preferencesButton.clicked.connect(self.preferencesShow)
        self.ui.refreshButton.clicked.connect(self.parser.scanAll)
        self.ui.collapseButton.clicked.connect(self.library.collapseAll)
        self.ui.expandButton.clicked.connect(self.library.expandAll)
        self.ui.libraryFilterLine.textChanged.connect(self.library.filterEvent)
        self.ui.libraryFilterClearButton.clicked.connect(self.ui.libraryFilterLine.clear)
        self.ui.slider.installEventFilter(self)

        self.setStatusBar(self.ui.statusBar)
        self.setWindowTitle("qoob")
        self.setWindowIcon(self.icon["qoob"])
        self.show()
        self._resumePlayback()

    def closeEvent(self, event):
        self.preferences.db["state"]["current tab"] = self.tabWidget.tabBar().currentIndex()
        self.preferences.db["state"]["playback position"] = self.player.position()
        self.preferences.db["state"]["current media state"] = self.player.state()
        self.preferences.db["state"]["current media"] = self.player.path
        self.preferences.save()

        playlist = {}
        for index in range(self.tabWidget.count() - 1):
            tabName = self.tabWidget.tabText(index)
            current = self.tabWidget.tabs[tabName]
            playlist[tabName] = {}
            playlist[tabName]["sort"] = (current["sort"].isChecked(), current["playlist"].sortColumn(), current["playlist"].header().sortIndicatorOrder())
            if current["playlist"].currentItem():
                playlist[tabName]["current"] = current["playlist"].currentItem().text(5)
            playlist[tabName]["files"] = []
            for item in range(current["playlist"].topLevelItemCount()):
                item = current["playlist"].topLevelItem(item)
                playlist[tabName]["files"].append(item.text(5))
        self.tabWidget.playlist.db = playlist
        self.tabWidget.playlist.save()
        self.parent.exit()

    def eventFilter(self, obj, event):
        if obj == self.ui.slider and event.type() == QtCore.QEvent.MouseButtonRelease:
            mouseEvent = QtGui.QMouseEvent(event)
            position = QtWidgets.QStyle.sliderValueFromPosition(obj.minimum(), obj.maximum(), mouseEvent.x(), obj.width())
            self.ui.slider.setValue(position)
            self.player.setPosition(obj.value())
        return QtCore.QObject.event(obj, event)

    def changeEvent(self, event):
        # Override minimize event
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                if self.preferences.get("general", "tray minimize") and self.preferences.get("general", "tray icon"):
                    self.setWindowState(QtCore.Qt.WindowNoState)
                    self.hide() if self.isVisible() else self.show()

    def _delete(self, files):
        self.action("delete")
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

            # Remove empty folder
            if self.preferences.get("general", "clean folder"):
                parent = os.path.abspath(os.path.join(f, os.pardir))
                if len(os.listdir(parent)) == 0:
                    os.rmdir(parent)
                    self.library.refresh()
                    return

            """
            # Remove item from library tree
            for item in range(self.library.topLevelItemCount()):
                item = self.library.topLevelItem(item)
                if self.library.deleteItem(item, f):
                    break
            """

    def _deletePrompt(self, files):
        if self.preferences.get("general", "delete confirm"):
            names = ""
            for f in files:
                names += "\n" + os.path.basename(f)
            msg = QtWidgets.QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Delete confirmation")
            msg.setText(f"Please confirm deletion of :\n{names}")
            msg.setStandardButtons(QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
            if msg.exec_() == QtWidgets.QMessageBox.Apply:
                self._delete(files)
        else:
            self._delete(files)

    def _findDefaultMusicFolder(self):
        xdgDirectories = os.path.expanduser("~/.config/user-dirs.dirs")
        if os.path.isfile(xdgDirectories):
            with open(xdgDirectories) as f:
                for line in f.read().splitlines():
                    line = line.split("=")
                    if line[0] == "XDG_MUSIC_DIR":
                        musicFolder = line[1].replace("$HOME", "~")
                        musicFolder = os.path.expanduser(musicFolder[1:-1])
                        self.preferences.db["music database"].append(musicFolder)
                        self.preferences.save()
                        break

    def _initStyle(self):
        self.icon = {}
        for icon in os.listdir(f"{LOCAL_DIR}icons"):
            iconName = os.path.splitext(icon)
            if iconName[1] == ".svg":
                self.icon[iconName[0]] = QtGui.QIcon(f"{LOCAL_DIR}icons/{icon}")
        self.ui.playButton.setIcon(self.icon["play"])
        self.ui.stopButton.setIcon(self.icon["stop"])
        self.ui.nextButton.setIcon(self.icon["next"])
        self.ui.previousButton.setIcon(self.icon["previous"])
        self.ui.shuffleButton.setIcon(self.icon["shuffle_off"])
        self.ui.preferencesButton.setIcon(self.icon["preferences"])
        self.ui.refreshButton.setIcon(self.icon["refresh"])
        self.ui.collapseButton.setIcon(self.icon["collapse"])
        self.ui.expandButton.setIcon(self.icon["expand"])

        # Init stylesheet
        iconPath = LOCAL_DIR + "icons/"
        stylesheet = f"QPushButton#libraryFilterClearButton {{ border-image: url({iconPath}filter_clear.svg); }}\n"
        stylesheet += f"QPushButton#libraryFilterClearButton:hover {{ border-image: url({iconPath}filter_hover.svg); }}"
        self.ui.libraryFilterClearButton.setStyleSheet(stylesheet)

    def _menuRefresh(self):
        self.menu.clear()
        if self.copied:
            self.menu.addAction(self.icon["paste"], "Paste selection", lambda: self.action("paste"))
        if self.tabWidget.current.selectedItems():
            self.menu.addAction(self.icon["cut"], "Cut selection", lambda: self.action("cut"))
            self.menu.addAction(self.icon["copy"], "Copy selection", lambda: self.action("copy"))
            if self.preferences.get("general", "file manager"):
                self.menu.addAction(self.icon["folder"], "Browse song folder", lambda: self.action("browse"))
            self.menu.addSeparator()
            self.menu.addAction(self.icon["remove"], "Delete from playlist", lambda: self.action("delete"))
            self.menu.addAction(self.icon["delete"], "Delete from disk", lambda: self.action("delete prompt"))

    def _resumePlayback(self):
        self.player.resumePlayback = self.preferences.get("general", "resume playback")
        playing = self.preferences.get("state", "current media state") == QtMultimedia.QMediaPlayer.PlayingState
        if self.player.resumePlayback and playing:
            self.player.setCurrentMedia(self.preferences.get("state", "current media"))

    def action(self, action):
        currentTab = self.tabWidget.current
        selection = currentTab.selectedItems()
        if action == "paste" and self.copied:
            for path in self.copied:
                item = currentTab.add(path)

            # Select pasted item
            currentTab.clearSelection()
            currentTab.setCurrentItem(item)

        elif selection:
            files = []
            for item in selection:
                files.append(item.text(5))

            if action == "copy":
                self.copied = files

            if action == "cut":
                self.copied = files
                self.action("delete")

            elif action == "delete":
                for item in selection:
                    index = currentTab.indexOfTopLevelItem(item)
                    currentTab.takeTopLevelItem(index)

                # Select next available item
                count = currentTab.topLevelItemCount()
                if index == count: index = count-1
                item = currentTab.topLevelItem(index)
                currentTab.clearSelection()
                currentTab.setCurrentItem(item)

            elif action == "delete prompt":
                self._deletePrompt(files)

            elif action == "browse":
                folder = os.path.abspath(os.path.join(currentTab.currentItem().text(5), os.pardir))
                cmd = f'{self.preferences.get("general", "file manager")} "{folder}"'
                self.process.startDetached(cmd)

    def libraryDone(self):
        self.library.addWildCard()
        self.ui.libraryFilterLine.setFocus(True)

    def librarySelect(self):
        self.player.lastPlayed = []
        self.tabWidget.current.sort()
        self.tabWidget.tabBar().setCurrentIndex(0)

    def menuShow(self):
        if self.tabWidget.current.selectedItems() or self.copied:
            self.menu.popup(QtGui.QCursor.pos())

    def parseCommands(self, cmd):
        if "play-pause" in cmd:
            self.player.playPauseEvent()

        elif "stop" in cmd:
            self.player.stopEvent()

        elif "previous" in cmd:
            self.player.previousEvent()

        elif "next" in cmd:
            self.player.nextEvent()

        elif "quit" in cmd:
            self.close()

        elif "delete" in cmd:
            self.action("delete prompt")

        elif "shuffle" in cmd:
            if len(cmd["shuffle"]) > 0:
                if cmd["shuffle"][0] == "on":
                    self.player.shuffleEvent(enable=True)
                elif cmd["shuffle"][0] == "off":
                    self.player.shuffleEvent(enable=False)
            else:
                self.player.shuffleEvent()
            self.popup.display("Shuffle enabled" if self.player.shuffle else "Shuffle disabled")

        elif "file" in cmd:
            if len(cmd["file"]) == 0:
                return False

            self.tabWidget.tabs["Library viewer"]["playlist"].clear()
            for f in cmd["file"]:
                if os.path.isfile(f):
                    self.tabWidget.tabs["Library viewer"]["playlist"].add(f)
            self.tabWidget.tabBar().setCurrentIndex(0)
            self.tabWidget.tabs["Library viewer"]["playlist"].sort()
            self.player.activateSelection()

        elif "folder" in cmd:
            if len(cmd["folder"]) == 0:
                return False

            self.tabWidget.tabs["Library viewer"]["playlist"].clear()
            for folder in cmd["folder"]:
                if os.path.isdir(folder):
                    for root, subfolder, files in os.walk(folder):
                        for f in files:
                            self.tabWidget.tabs["Library viewer"]["playlist"].add(f"{root}/{f}")
            self.tabWidget.tabBar().setCurrentIndex(0)
            self.tabWidget.tabs["Library viewer"]["playlist"].sort()
            self.player.activateSelection()

        elif cmd:
            self.log.error(f"Unkown command: {cmd}")
            return False
        return True

    def preferencesSave(self):
        self.preferencesForm.settingsSave()
        oldDb = self.preferences.get("music database")
        newDb = self.preferencesForm.db["music database"]
        changed = not oldDb == newDb

        self.preferences.db = tools.copyDict(self.preferencesForm.db)
        self.preferences.save()
        for path in oldDb:
            if path not in newDb:
                self.parser.removeDatabase(path)
        if changed:
            self.parser.scanAll()

        self.popup.updateView()
        if self.preferences.get("general", "tray icon"):
            self.trayIcon.show()
        else:
            self.trayIcon.hide()

    def preferencesShow(self):
        self.preferencesForm.show()
        self.preferencesForm.raise_()

    def setItemColor(self, color):
        current = self.tabWidget.current.currentItem()
        if current:
            self.tabWidget.current.currentItem().setColor(color)

    def setStatusMessage(self, left, right):
        if left:
            self.ui.statusBar.showMessage(left)
        if right:
            self.ui.statusRightLabel.setText(right)


def main(cmd=""):
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    gui = Main(app)
    gui.parseCommands(cmd)
    bus = tools.QDBusObject(parent=gui)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
