#!/usr/bin/python3
import datetime
import json
import os
import sys
from PyQt5 import QtGui, QtWidgets, QtCore, uic

try:
    import qoob.backend.tools as tools
    import qoob.ui.preferences
except ImportError:
    import backend.tools as tools

# Init common settings
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
CONFIG_DIR = os.path.expanduser("~/.config/qoob/")
PREFERENCES_FILE = CONFIG_DIR + "preferences.json"

PREFERENCES_DEFAULT = \
{
    'general':
    {
        'resume playback': True,
        'delete confirm': True,
        'clean folder': True,
        'file manager': 'spacefm --no-saved-tabs',
        'tray icon': True,
        'tray minimize': True,
        'popup': True,
    },
    'viewer':
    {
        'expand library': True,
        'strip titles': True,
        'title format': '%title% (%artist%) - qoob',
        'notification format': '%artist%\n\'%title%\'',
        'sorting routine': ['Track (Ascending)', 'Album (Ascending)', 'Artist (Ascending)', 'Disable sorting'],
        'sort by default': False,
    },
    'popup':
    {
        'opacity': 0.8,
        'font size': 9,
        'font family': 'Sans Serif',
        'width': 250,
        'height': 75,
        'duration': 2,
        'position': 'bottom right',
        'vertical offset': -15,
        'horizontal offset': -20,
        'foreground': 'white',
        'background': 'black',
    },
    'state':
    {
        'current tab': 0,
        'playback position': 0,
        'current media state': 0,
        'current media': '',
    },
    'music database': [],
}


class PreferencesDatabase(object):
    def __init__(self, parent):
        self.log = parent.logger.new(name="Preferences")
        if os.path.isfile(PREFERENCES_FILE) and os.stat(PREFERENCES_FILE).st_size > 0:
            self.load()
            if not set(PREFERENCES_DEFAULT) == set(self.db):
                missing = str(list(filter(lambda x: x not in self.db, PREFERENCES_DEFAULT)))
                self.log.error(f"Preferences KeyError: {missing}")
                self.log.warning("Restored preferences to default")
                self.db = tools.copyDict(PREFERENCES_DEFAULT)
                self.save()
        else:
            if not os.path.isdir(CONFIG_DIR):
                os.mkdir(CONFIG_DIR)
            self.db = tools.copyDict(PREFERENCES_DEFAULT)
            with open(PREFERENCES_FILE, "w") as f:
                f.write(json.dumps(self.db, indent=2, sort_keys=False))
            self.log.info("Created preferences file")

    def get(self, *keys, db=None, fault=False):
        if not db: db = self.db
        for key in keys:
            try:
                db = db[key]
            except TypeError:
                pass
            except KeyError:
                if fault:
                    self.log.critical(f"Preferences KeyError: '{key}' not found in default database")
                    return None
                self.log.error(f"Preferences KeyError: '{key}' not found")

                backup = PREFERENCES_FILE + ".broken"
                with open(backup, "w") as f:
                    f.write(json.dumps(self.db, indent=2, sort_keys=False))
                msg = "Preferences have been reset to default. This is\n" \
                    + "most likely caused by a backward incompatibility.\n" \
                    + f"A backup of the old configuration is saved at:\n\n{backup}"
                error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Broken preferences error", msg)
                error.exec_()

                self.log.warning("Restored preferences to default")
                self.db = tools.copyDict(PREFERENCES_DEFAULT)
                self.save()
                return self.get(*keys, fault=True)
        return db

    def load(self):
        with open(PREFERENCES_FILE, "r") as f:
            self.db = json.load(f)
        self.log.info("Loaded preferences database")

    def save(self):
        with open(PREFERENCES_FILE, "w") as f:
            f.write(json.dumps(self.db, indent=2, sort_keys=False))
        self.log.info("Saved preferences database")


class PreferencesForm(QtWidgets.QDialog):
    resetMetadata = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        # Load the ui file in case the gui modules are not loaded
        if "qoob.ui.preferences" in sys.modules:
            self.ui = qoob.ui.preferences.Ui_Dialog()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + '../ui/preferences.ui', self)
        self.setFixedSize(600, 480)

        self.parent = parent
        self.log = parent.logger.new(name="Preferences")
        self.preferences = parent.preferences
        self.icon = parent.icon
        self._settingsInit()
        try:
            self._settingsLoad()
        except KeyError:
            self.log.error("KeyError in preferences database, loaded default settings instead")
            self._settingsReset()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def showEvent(self, event):
        self.db = tools.copyDict(self.preferences.db)
        self._settingsLoad()
        event.accept()

    def _dbAddButton(self, path=None):
        if not path:
            path = self.ui.dbLine.text()
        if os.path.isdir(path):
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, path)
            item.setText(1, "")
            self.ui.dbTree.addTopLevelItem(item)
            self.ui.dbLine.setText("")

    def _dbBrowseButton(self):
        browser = QtWidgets.QFileDialog()
        browser.setFileMode(QtWidgets.QFileDialog.Directory)
        browser.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if browser.exec_():
            self.ui.dbLine.setText(browser.selectedFiles()[0])

    def _dbDeleteButton(self):
        row = self.ui.dbTree.currentIndex().row()
        if row > -1:
            item = self.ui.dbTree.takeTopLevelItem(row)
            path = item.text(0)
            self.ui.dbLine.setText(path)

    def _dbResetButton(self):
        self.resetMetadata.emit()

    def _popupColorChanged(self, layer):
        color = self.colorWidget.currentColor()
        self.db["parameters"]["popup"][layer] = color.name()

    def _popupPickColor(self, color, layer=None):
        self.colorWidget = QtWidgets.QColorDialog(QtGui.QColor(color))
        self.colorWidget.setWindowFlags(self.colorWidget.windowFlags() | Qt.WindowStaysOnTopHint)
        self.colorWidget.currentColorChanged.connect(lambda: self._popupColorChanged(layer))
        self.colorWidget.exec_()
        return self.colorWidget.selectedColor()

    def _popupPickLayerColor(self, layer):
        currentColor = self.db["parameters"]["popup"][layer]
        color = self._popupPickColor(currentColor, layer)
        if not color.isValid():
            color = QtGui.QColor(currentColor)
        self.db["parameters"]["popup"][layer] = color.name()

    def _settingsInit(self):
        self.db = tools.copyDict(self.preferences.db)

        # General settings
        self.ui.resetButton.clicked.connect(self._settingsReset)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.accepted.emit)
        self.ui.sideMenuList.selectionModel().selectionChanged.connect(self._settingsMenuSelect)

        # Library database
        self.ui.dbAddButton.clicked.connect(self._dbAddButton)
        self.ui.dbDeleteButton.clicked.connect(self._dbDeleteButton)
        self.ui.dbBrowseButton.clicked.connect(self._dbBrowseButton)
        self.ui.dbResetButton.clicked.connect(self._dbResetButton)

        # Library viewer
        self.ui.sortAddButton.clicked.connect(self._sortAddButton)
        self.ui.sortRemoveButton.clicked.connect(self._sortRemoveButton)

        # Notifications
        self.ui.popupBackgroundButton.clicked.connect(lambda: self._popupPickLayerColor("background"))
        self.ui.popupForegroundButton.clicked.connect(lambda: self._popupPickLayerColor("foreground"))

    def _settingsLoad(self):
        # General settings
        self.ui.resumePlaybackBox.setChecked(self.db["general"]["resume playback"])
        self.ui.deleteConfirmBox.setChecked(self.db["general"]["delete confirm"])
        self.ui.cleanFolderBox.setChecked(self.db["general"]["clean folder"])
        self.ui.fileManagerLine.setText(self.db["general"]["file manager"])
        self.ui.trayIconBox.setChecked(self.db["general"]["tray icon"])
        self.ui.trayMinimizeBox.setChecked(self.db["general"]["tray minimize"])
        self.ui.popupEnableBox.setChecked(self.db["general"]["popup"])

        # Library database
        self.ui.dbResetButton.setIcon(self.icon["reset"])
        self.ui.dbTree.clear()
        for folder in self.db["music database"]:
            self._dbAddButton(folder)

        # Library viewer
        self.ui.expandLibraryBox.setChecked(self.db["viewer"]["expand library"])
        self.ui.stripTitlesBox.setChecked(self.db["viewer"]["strip titles"])
        self.ui.titleFormatLine.setText(self.db["viewer"]["title format"])
        self.ui.notificationFormatLine.setText(self.db["viewer"]["notification format"])
        self.ui.sortByDefaultBox.setChecked(self.db["viewer"]["sort by default"])

        self.ui.sortAvailableList.clear()
        self.ui.sortSelectedList.clear()
        self.ui.sortSelectedList.addItems(self.db["viewer"]["sorting routine"])
        sortActions = ("Artist (Ascending)", "Artist (Descending)", "Album (Ascending)", "Album (Descending)", "Track (Ascending)", "Track (Descending)", "Title (Ascending)", "Title (Descending)", "Duration (Ascending)", "Duration (Descending)", "Disable sorting")
        for item in sortActions:
            if item not in self.db["viewer"]["sorting routine"]:
                self.ui.sortAvailableList.addItem(item)

        # Notifications
        self.ui.popupFontSizeBox.setValue(self.db["popup"]["font size"])
        self.ui.popupFontFamilyCombo.setCurrentText(self.db["popup"]["font family"])
        self.ui.popupOpacityBox.setValue(self.db["popup"]["opacity"])
        self.ui.popupWidthBox.setValue(self.db["popup"]["width"])
        self.ui.popupHeightBox.setValue(self.db["popup"]["height"])
        self.ui.popupDurationBox.setValue(self.db["popup"]["duration"])
        self.ui.popupVOffsetBox.setValue(self.db["popup"]["vertical offset"])
        self.ui.popupHOffsetBox.setValue(self.db["popup"]["horizontal offset"])

        position = self.db["popup"]["position"]
        if position == "top left":
            self.ui.topLeftRadio.setChecked(True)
        elif position == "top center":
            self.ui.topCenterRadio.setChecked(True)
        elif position == "top right":
            self.ui.topRightRadio.setChecked(True)
        elif position == "middle left":
            self.ui.middleLeftRadio.setChecked(True)
        elif position == "middle center":
            self.ui.middleCenterRadio.setChecked(True)
        elif position == "middle right":
            self.ui.middleRightRadio.setChecked(True)
        elif position == "bottom left":
            self.ui.bottomLeftRadio.setChecked(True)
        elif position == "bottom center":
            self.ui.bottomCenterRadio.setChecked(True)
        elif position == "bottom right":
            self.ui.bottomRightRadio.setChecked(True)

    def _settingsMenuSelect(self):
        index = self.ui.sideMenuList.currentRow()
        self.ui.stackedWidget.setCurrentIndex(index)

    def _settingsReset(self):
        self.db = tools.copyDict(PREFERENCES_DEFAULT)
        self._settingsLoad()

    def _sortAddButton(self):
        item = self.ui.sortAvailableList.currentItem()
        if item:
            row = self.ui.sortAvailableList.currentRow()
            item = self.ui.sortAvailableList.takeItem(row)
            self.ui.sortSelectedList.addItem(item)

    def _sortRemoveButton(self):
        row = self.ui.sortSelectedList.currentRow()
        item = self.ui.sortSelectedList.takeItem(row)
        if item:
            self.ui.sortAvailableList.addItem(item)

    @QtCore.pyqtSlot(str)
    def dbDoneSlot(self, path):
        for folder in range(self.ui.dbTree.topLevelItemCount()):
            item =  self.ui.dbTree.topLevelItem(folder)
            if item.text(0) == path:
                now = datetime.datetime.now()
                item.setText(1, f"Done ({now.day}-{now.strftime('%b')} {now.strftime('%H:%M:%S')})")

    @QtCore.pyqtSlot(str)
    def dbStartSlot(self, path):
        for folder in range(self.ui.dbTree.topLevelItemCount()):
            item =  self.ui.dbTree.topLevelItem(folder)
            if item.text(0) == path:
                item.setText(1, "Scanning")

    @QtCore.pyqtSlot()
    def setPending(self):
        for folder in range(self.ui.dbTree.topLevelItemCount()):
            item =  self.ui.dbTree.topLevelItem(folder)
            item.setText(1, "Pending")

    @QtCore.pyqtSlot()
    def settingsSave(self):
        # General Settings
        self.db["general"]["resume playback"] = self.ui.resumePlaybackBox.isChecked()
        self.db["general"]["delete confirm"] = self.ui.deleteConfirmBox.isChecked()
        self.db["general"]["clean folder"] = self.ui.cleanFolderBox.isChecked()
        self.db["general"]["file manager"] = self.ui.fileManagerLine.text()
        self.db["general"]["tray icon"] = self.ui.trayIconBox.isChecked()
        self.db["general"]["tray minimize"] = self.ui.trayMinimizeBox.isChecked()
        self.db["general"]["popup"] = self.ui.popupEnableBox.isChecked()

        # Library database
        musicDatabase = []
        for item in range(self.ui.dbTree.topLevelItemCount()):
            item = self.ui.dbTree.topLevelItem(item)
            musicDatabase.append(item.text(0))
        self.db["music database"] = musicDatabase

        # Library viewer
        self.db["viewer"]["expand library"] = self.ui.expandLibraryBox.isChecked()
        self.db["viewer"]["strip titles"] = self.ui.stripTitlesBox.isChecked()
        self.db["viewer"]["title format"] = self.ui.titleFormatLine.text()
        self.db["viewer"]["notification format"] = self.ui.notificationFormatLine.text()
        self.db["viewer"]["sort by default"] = self.ui.sortByDefaultBox.isChecked()
        sortingRoutine = []
        for item in range(self.ui.sortSelectedList.count()):
            sortingRoutine.append(self.ui.sortSelectedList.item(item).text())
        self.db["viewer"]["sorting routine"] = sortingRoutine

        # Notifications
        self.db["popup"]["enable"] = self.ui.popupEnableBox.isChecked()
        self.db["popup"]["font size"] = self.ui.popupFontSizeBox.value()
        self.db["popup"]["font family"] = self.ui.popupFontFamilyCombo.currentText()
        self.db["popup"]["opacity"] = self.ui.popupOpacityBox.value()
        self.db["popup"]["width"] = self.ui.popupWidthBox.value()
        self.db["popup"]["height"] = self.ui.popupHeightBox.value()
        self.db["popup"]["duration"] = self.ui.popupDurationBox.value()
        self.db["popup"]["vertical offset"] = self.ui.popupVOffsetBox.value()
        self.db["popup"]["horizontal offset"] = self.ui.popupHOffsetBox.value()

        if self.ui.topLeftRadio.isChecked():
            position = "top left"
        elif self.ui.topCenterRadio.isChecked():
            position = "top center"
        elif self.ui.topRightRadio.isChecked():
            position = "top right"
        elif self.ui.middleLeftRadio.isChecked():
            position = "middle left"
        elif self.ui.middleCenterRadio.isChecked():
            position = "middle center"
        elif self.ui.middleRightRadio.isChecked():
            position = "middle right"
        elif self.ui.bottomLeftRadio.isChecked():
            position = "bottom left"
        elif self.ui.bottomCenterRadio.isChecked():
            position = "bottom center"
        elif self.ui.bottomRightRadio.isChecked():
            position = "bottom right"
        self.db["popup"]["position"] = position
