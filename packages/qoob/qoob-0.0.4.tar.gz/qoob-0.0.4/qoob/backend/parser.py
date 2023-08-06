#!/usr/bin/python3
import os
import re
import sys

from PyQt5 import QtWidgets, QtCore
import mutagen

try:
    import qoob.backend.tools as tools
except ImportError:
    import backend.tools as tools

mappings = \
{
    "artist": ("TPE0", "TPE1", "TPE2", u"©ART", "Author", "Artist", "ARTIST", "artist", "TRACK ARTIST", "TRACKARTIST", "TrackArtist", "Track Artist"),
    "album": ("TALB", "ALBUM", "Album", u"©alb", "album"),
    "track": ("TRCK", "TRACKNUMBER", "Track", "trkn", "tracknumber"),
    "title": ("TIT2", "TITLE", "Title", u"©nam", "title"),
}

allowedFileTypes = (".mp3", ".flac", ".ogg", ".m4a", ".wav")
def allowedType(path):
    ext = os.path.splitext(path)[1].lower()
    return (ext in allowedFileTypes)


class Parser(QtCore.QObject):
    setFilterEnable = QtCore.pyqtSignal(bool)
    addAlbum = QtCore.pyqtSignal(object, str)
    addArtist = QtCore.pyqtSignal(object)
    startDb = QtCore.pyqtSignal(str)
    doneDb = QtCore.pyqtSignal(str)
    pending = QtCore.pyqtSignal()
    done = QtCore.pyqtSignal()
    clear = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.log = parent.logger.new("Parser")
        self.preferences = parent.preferences
        self.metadata = tools.Database("metadata")
        self.trackPattern = re.compile(r"\b\d{2}\b|\b\d{2}(?=\D)")

    def _cleanMetadata(self):
        for path in dict(self.metadata.db):
            if not os.path.exists(path):
                del self.metadata.db[path]

    def _fillHeader(self, header, tags):
        title, artist, album, track = tags

        if "artist" not in header:
            header["artist"] = artist

        if "album" not in header:
            header["album"] = album

        if "track" not in header:
            header["track"] = track

        if "title" not in header:
            if self.preferences.get("viewer", "strip titles"):
                title = re.sub(r"\W*" + artist + r"\W*", "", title, flags=re.IGNORECASE, count=1)
                title = re.sub(r"\W*" + album + r"\W*", "", title, flags=re.IGNORECASE, count=1)
                title = re.sub(r"\W*" + track + r"\W*", self._trackChar, title, flags=re.IGNORECASE, count=1)
                header["title"] = title
            else:
                header["title"] = re.sub(r"\W*" + track + r"\W*", self._trackChar, title, flags=re.IGNORECASE, count=1)
        return header

    def _guessFileHeader(self, path):
        basename = os.path.basename(path)
        title = os.path.splitext(basename)[0]

        # Fetch album and artist from path
        album = os.path.abspath(os.path.join(path, os.pardir))
        artist = os.path.abspath(os.path.join(album, os.pardir))
        album = os.path.basename(album)
        artist = os.path.basename(artist)

        # Fetch track number from title,
        # remove artist/album in case it contain two digits numbers
        track = re.sub(r"\W*" + artist + r"\W*", "", title, flags=re.IGNORECASE, count=1)
        track = re.sub(r"\W*" + album + r"\W*", "", track, flags=re.IGNORECASE, count=1)
        track = re.search(self.trackPattern, track)
        track = track.group() if track else ""
        return (title, artist, album, track)

    def _hasAudioFiles(self, path):
        for root, subfolders, files in os.walk(path):
            for f in files:
                if allowedType(f):
                    return True
        return False

    def _item(self, path, node):
        name = os.path.splitext(os.path.basename(path))[0]
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, path)
        return item

    def _parseHeaderTag(self, header, key, tag):
        if isinstance(header, mutagen.flac.FLAC) or isinstance(header, mutagen.oggvorbis.OggVorbis):
            header = dict(header)

        header = header[tag][-1]
        if isinstance(header, tuple):
            header = str(header[0])

        if key == "track":
            return header.split("/")[0]
        return header

    def _readHeader(self, path):
        tags = {"duration": "?"}
        header = None
        try:
            header = mutagen.File(path)
        except:
            tags["error"] = f"{sys.exc_info()[0]} {sys.exc_info()[1]}"
            self.log.warning(f"{path}\n{sys.exc_info()[0]} {sys.exc_info()[1]}\n")

        if header:
            if header.info:
                s = int(header.info.length)
                m, s = divmod(s, 60)
                h, m = divmod(m, 60)
                tags["duration"] = "%02d:%02d:%02d" % (h, m, s)

            for key in ("artist", "album", "track", "title"):
                for tag in mappings[key]:
                    try:
                        tags[key] = self._parseHeaderTag(header, key, tag)
                        break
                    except KeyError:
                        pass
        return tags

    def _recursiveScan(self, folder, node=None):
        try:
            for f in os.listdir(folder):
                path = os.path.join(folder, f)

                if os.path.isdir(path):
                    if self._hasAudioFiles(path):
                        item = self._item(path, node=node)
                        if node:
                            self.addAlbum.emit(node, path)
                        else:
                            self.addArtist.emit(item)
                        self._recursiveScan(path, node=item)

                elif allowedType(path):
                    if path not in self.metadata.db:
                        self.metadata.db[path] = self.header(path)
        except PermissionError:
            pass

    def _trackChar(self, match):
        return "" if match.start() == 0 else " - "

    @QtCore.pyqtSlot(str)
    def header(self, path):
        if path in self.metadata.db:
            return self.metadata.db[path]

        header = self._readHeader(path)
        if set({"artist", "album", "track", "title"}) - set(header):
            tags = self._guessFileHeader(path)
            header = self._fillHeader(header, tags)
        return header

    @QtCore.pyqtSlot(str)
    def removeDatabase(self, folder):
        for path in dict(self.metadata.db):
            if path.startswith(folder):
                del self.metadata.db[path]
        self.scanAll()

    @QtCore.pyqtSlot()
    def reset(self):
        self.metadata.db = {}
        self.scanAll()

    @QtCore.pyqtSlot()
    def scanAll(self):
        self.setFilterEnable.emit(False)
        self.clear.emit()
        self.pending.emit()
        self._cleanMetadata()
        for folder in self.preferences.get("music database"):
            self.startDb.emit(folder)
            self._recursiveScan(folder)
            self.doneDb.emit(folder)
            self.metadata.save()
        self.setFilterEnable.emit(True)
        self.done.emit()

