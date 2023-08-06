#!/usr/bin/python3
import os
from PyQt5 import QtGui, QtWidgets, QtCore

try:
    import qoob.backend.tools as tools
    import qoob.backend.parser as parser
except ImportError:
    import backend.tools as tools
    import backend.parser as parser

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
DB_DIR = os.path.expanduser("~/.config/qoob/")


class SortBox(QtWidgets.QCheckBox):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setText("Enable sorting")
        self.clicked.connect(self._toggle)
        if parent.preferences.get("viewer", "sort by default"):
            self.setChecked(True)

    def _toggle(self):
        self.parent.tabWidget.current.setSortingEnabled(self.isChecked())


class Tabs(QtWidgets.QTabWidget):
    action = QtCore.pyqtSignal(str)
    changed = QtCore.pyqtSignal()
    play = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.preferences = parent.preferences

        iconPath = LOCAL_DIR + "../icons/"
        stylesheet = f"QTabBar::close-button {{ image: url({iconPath}tab_close.svg); }}\n"
        stylesheet += f"QTabBar::close-button:hover {{ image: url({iconPath}tab_hover.svg); }}\n"
        self.setStyleSheet(stylesheet)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.addTab(self.tab1, "Library viewer")
        self.addTab(self.tab2, "")

        self.setTabEnabled(1, False)
        self.dummyButton = QtWidgets.QPushButton()
        self.dummyButton.setFixedSize(0, 0)
        self.newButton = QtWidgets.QPushButton()
        self.newButton.setFlat(True)
        self.newButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.newButton.setFixedSize(30, 20)
        self.newButton.setIcon(self.parent.icon["tab_add"])
        self.newButton.clicked.connect(self._add)
        self.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, self.dummyButton)
        self.tabBar().setTabButton(1, QtWidgets.QTabBar.RightSide, self.newButton)

        self.tabCloseRequested.connect(self._close)
        self.currentChanged.connect(self._changed)
        self.installEventFilter(self)
        self.tabBar().installEventFilter(self)

        self.tabs = {}
        self.tabs["Library viewer"] = {"playlist": Tree(parent), "sort": SortBox(parent)}
        self.current = self.tabs["Library viewer"]["playlist"]

        self.viewLayout = QtWidgets.QGridLayout()
        self.viewLayout.addWidget(self.tabs["Library viewer"]["playlist"])
        self.viewLayout.addWidget(self.tabs["Library viewer"]["sort"])
        self.currentWidget().setLayout(self.viewLayout)

        self._playlistsLoad()

    def eventFilter(self, obj, event):
        if obj == self.tabBar() and event.type() == QtCore.QEvent.MouseButtonDblClick:
            self._rename()

        elif obj == self and event.type() == QtCore.QEvent.ShortcutOverride:
            ctrl = (event.modifiers() == QtCore.Qt.ControlModifier)
            if ctrl and event.key() == QtCore.Qt.Key_C:
                self.action.emit("copy")
            if ctrl and event.key() == QtCore.Qt.Key_X:
                self.action.emit("cut")
            elif ctrl and event.key() == QtCore.Qt.Key_V:
                self.action.emit("paste")
            elif event.key() == QtCore.Qt.Key_Backspace:
                self.action.emit("delete")
            elif event.key() == QtCore.Qt.Key_Delete:
                self.action.emit("delete prompt")
            elif event.key() == QtCore.Qt.Key_Space:
                self.play.emit()
        return QtCore.QObject.event(obj, event)

    def _add(self, name=None):
        layout = QtWidgets.QVBoxLayout()
        tab = QtWidgets.QWidget(self)
        count = self.tabBar().count()
        index = 1
        if not name:
            name = "Playlist " + str(index)
        while name in self.tabs:
            index += 1
            name = "Playlist " + str(index)
        self.tabs[name] = {}
        self.tabs[name] = {"playlist": Tree(self.parent), "sort": SortBox(self.parent)}
        self.tabs[name]["playlist"].setSortingEnabled(self.tabs[name]["sort"].isChecked())
        self.addTab(tab, name)
        self.setCurrentWidget(tab)
        self.tabBar().moveTab(count - 1, count)
        self.currentWidget().setLayout(layout)
        layout.addWidget(self.tabs[name]["playlist"])
        layout.addWidget(self.tabs[name]["sort"])

    def _changed(self, index):
        tabName = self.tabText(index)
        if tabName:
            self.current = self.tabs[tabName]["playlist"]
            self.changed.emit()

    def _close(self, tab):
        tabName = self.tabText(tab)
        del self.tabs[tabName]
        if tabName in self.playlist.db:
            del self.playlist.db[tabName]
            self.playlist.save()
        self.removeTab(tab)

        # Prevent landing on the '+' tab
        count = self.tabBar().count() - 1
        if count == self.tabBar().currentIndex():
            self.tabBar().setCurrentIndex(count - 1)

    def _playlistsLoad(self):
        self.playlist = tools.Database("playlist")
        for tabName in self.playlist.db:
            if not tabName == "Library viewer":
                self._add(tabName)

            # Load sorting option
            sort = self.playlist.db[tabName]["sort"]
            self.tabs[tabName]["playlist"].sortByColumn(sort[1], sort[2])
            self.tabs[tabName]["sort"].setChecked(sort[0])
            self.tabs[tabName]["playlist"].setSortingEnabled(sort[0])

            # Load files
            for path in self.playlist.db[tabName]["files"]:
                item = self.tabs[tabName]["playlist"].add(path, append=True)
                if "current" in self.playlist.db[tabName] and path == self.playlist.db[tabName]["current"]:
                    self.tabs[tabName]["playlist"].setCurrentItem(item)
        self.tabBar().setCurrentIndex(self.preferences.get("state", "current tab"))

    def _rename(self):
        tabIndex = self.tabBar().currentIndex()
        oldName = self.tabText(tabIndex)
        if not oldName == "Library viewer":
            newName = self._renamePrompt(oldName)
            if newName and newName not in self.tabs:
                self.tabs[newName] = self.tabs.pop(oldName)
                if oldName in self.playlist.db:
                    self.playlist.db[newName] = self.playlist.db.pop(oldName)
                    self.playlist.save()
                self.setTabText(tabIndex, newName)

    def _renamePrompt(self, oldName):
        msg = QtWidgets.QInputDialog()
        msg.setInputMode(QtWidgets.QInputDialog.TextInput)
        msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        msg.setWindowTitle(f"Rename '{oldName}'")
        msg.setLabelText("Enter the new name:")
        msg.setTextValue(oldName)
        msg.setFixedSize(250, 100)
        accept = msg.exec_()
        newName = msg.textValue()
        if accept and newName:
            return newName


class Tree(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.preferences = parent.preferences
        self.metadata = parent.parser.metadata

        self.setHeaderLabels(["Artist", "Album", "Track", "Title", "Duration"])
        self.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.header().setStretchLastSection(False)
        self.setAlternatingRowColors(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(parent.menuShow)
        self.itemActivated.connect(parent.player.activateSelection)
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(4, 80)

    def add(self, path, append=False):
        basename = os.path.basename(path)
        extension = os.path.splitext(basename)[1].lower()
        if extension in parser.allowedFileTypes:
            tags = self.parent.parser.header(path)
            item = TreeItem()
            item.setText(0, tags["artist"])
            item.setText(1, tags["album"])
            item.setText(2, tags["track"])
            item.setText(3, tags["title"])
            item.setText(4, tags["duration"])
            item.setText(5, path)

            if append:
                self.addTopLevelItem(item)
            else:
                index = self.currentIndex().row()
                if index == -1: index = 0
                self.insertTopLevelItem(index, item)
            return item

    def sort(self):
        headers = {"Artist": 0, "Album": 1, "Track": 2, "Title": 3, "Duration": 4}
        sortingRoutine = []

        for action in self.preferences.get("viewer", "sorting routine"):
            if action == "Disable sorting":
                self.parent.tabWidget.tabs["Library viewer"]["sort"].setChecked(False)
                self.setSortingEnabled(False)
            else:
                self.parent.tabWidget.tabs["Library viewer"]["sort"].setChecked(True)
                action = action.split()
                header = headers[action[0]]
                if action[1] == "(Ascending)":
                    direction = QtCore.Qt.AscendingOrder
                elif action[1] == "(Descending)":
                    direction = QtCore.Qt.DescendingOrder
                self.setSortingEnabled(True)
                self.sortByColumn(header, direction)


class TreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(self.flags() &~ QtCore.Qt.ItemIsDropEnabled)
        self.lastColor = "none"

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        try:
            return int(key1) < int(key2)
        except ValueError:
            return key1.lower() < key2.lower()

    def setColor(self, color):
        priority = {"none": 0, "green": 0, "yellow": 1, "red": 2}
        if priority[color] >= priority[self.lastColor]:
            self.lastColor = color
            try:
                for column in range(5):
                    if color == "none":
                        self.setData(column, QtCore.Qt.BackgroundRole, None)
                        self.setData(column, QtCore.Qt.ForegroundRole, None)
                    elif color == "green":
                        self.setForeground(column, QtGui.QColor("#004000"))
                        self.setBackground(column, QtGui.QColor("#c6efce"))
                    elif color == "yellow":
                        self.setForeground(column, QtGui.QColor("#553400"))
                        self.setBackground(column, QtGui.QColor("#ffeb9c"))
                    elif color == "red":
                        self.setForeground(column, QtGui.QColor("#9c0006"))
                        self.setBackground(column, QtGui.QColor("#ffc7ce"))
            except RuntimeError:
                pass


